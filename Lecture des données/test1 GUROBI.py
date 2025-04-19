import gurobipy as gp
from gurobipy import GRB
from datetime import datetime, timedelta
import csv
import itertools
from datetime import datetime, timedelta

# Importez vos fonctions et classes personnalisées
from tasksCreator import generate_tasks_lists
from rosterCreator import generate_rosters_list
from allPairings import all_pairings
from does_planning_respect_repos import check_planning_conges

# Votre fonction de test de faisabilité temporelle
def test_if_task_fits(first_task, second_task, new_task) -> bool:
    if not new_task['start'] or not new_task['end']:
        return False
    return first_task['end'] < new_task['start'] and \
           new_task['end'] < second_task['start'] and \
           second_task['start'] >= new_task['rpcexactdate'] and \
           new_task['racexactdate'] >= first_task['end'] and \
           new_task['start'].month == 6 and new_task['end'].month == 6 and \
           new_task['start'].year == 2024 and new_task['end'].year == 2024

# Génération des tâches
pairings_tasks, ground_activity_tasks, standby_tasks = generate_tasks_lists()

# Constructions des dictionnaires pour faciliter l'accès (si besoin)
pairings_tasks_dict = {task.id: task for task in pairings_tasks}
ground_tasks_dict   = {task.ground_activity_number: task for task in ground_activity_tasks}
standby_tasks_dict  = {task.standby_number: task for task in standby_tasks}

# Récupération des rosters
rosters = generate_rosters_list()

# Dictionnaire des pairings (pour récupérer par exemple un block period)
all_pairings_dict = all_pairings()




model = gp.Model("CrewAssignment")

#définition de "c(p,r), o(i,r) en fonction du type de PN"
x_pairing = {}
for p in rosters:
    for r in pairings_tasks:
        # On n'envisage l'affectation que si le type de crew du roster correspond au type requis de la tâche
        if p.crew_type == r.type_place:
            var_name = f"x_pairing_{p.fcNumber}_{r.id}"
            x_pairing[(p, r)] = model.addVar(vtype=GRB.BINARY, name=var_name)

model.update()

#Ajout des contraintes

# Chaque rotation contient au plus un CDG et 2 OPL
for r in pairings_tasks:
    if r.type_place == "CDB":
        model.addConstr(
            gp.quicksum(x_pairing.get((p, r), 0) for p in rosters if p.crew_type == "CDB") <= 1,
            name=f"assign_pairing_{r.id}_CDB"
        )
    elif r.type_place == "OPL":
        model.addConstr(
            gp.quicksum(x_pairing.get((p, r), 0) for p in rosters if p.crew_type == "OPL") <= 2,
            name=f"assign_pairing_{r.id}_OPL"
        )

#Contrainte sur la non-superposition des pairings
Lr = set()

# Parcours de toutes les paires distinctes de tâches
for task1, task2 in itertools.combinations(pairings_tasks, 2):
    # Ne considérer que les tâches du même type, ici "OPL" ou "CDB"
    if task1.type_place == task2.type_place and task1.type_place in ["OPL", "CDB"]:
        # Vérification du chevauchement
        # Deux tâches se chevauchent si task1.start < task2.end et task2.start < task1.end
        if (task1.rpc_exact_date > task2.start or task1.end > task2.rac_exact_date) or (task1.start < task2.rpc_exact_date or task1.rac_exact_date < task2.end):
            # On ajoute la paire (ordre indépendant) à l'ensemble Lr.
            # Pour éviter les doublons, on peut utiliser un tuple trié (si les tâches sont comparables ou on utilise leurs identifiants)
            Lr.add((task1, task2))


# Pour chaque paire (t1, t2) dans Lr et pour chaque roster de type compatible (par exemple "OPL" ou "CDB"),
# on impose que le roster ne puisse être affecté qu'à l'une des deux tâches.
for (r1, r2) in Lr:
    # On suppose que t1 et t2 sont de même type, donc on peut tester par exemple sur t1.type_place.
    for p in rosters:
        if p.crew_type == r1.type_place:
            # On ajoute la contrainte seulement si les variables existent pour ce roster et ces tâches
            if (p, r1) in x_pairing and (p, r2) in x_pairing:
                model.addConstr(
                    x_pairing[(p, r1)] + x_pairing[(p, r2)] <= 1,
                    name=f"no_double_{p.fcNumber}_{r1.id}_{r2.id}"
                )

#Définition de l'objectif
objective = gp.quicksum(max((x_pairing[(p, r)] * (r.end-r.start).total_seconds() - 30*3600),0)- (x_pairing[(p,r)]*(r.end-r.start)) for (p, r) in x_pairing)

model.setObjective(objective, GRB.MINIMIZE)
model.optimize()

if model.status == GRB.OPTIMAL:
    print("Solution optimale trouvée :")
    for (p, r), var in x_pairing.items():
        if var.X > 0.5:  # Pour une variable binaire
            print(f"Roster {p.fcNumber} est affecté à la pairing task {r.id} de {r.start} à {r.end}")

    