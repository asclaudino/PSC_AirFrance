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



# Génération des tâches
pairings_tasks, ground_activity_tasks, standby_tasks = generate_tasks_lists()

# Constructions des dictionnaires pour faciliter l'accès (si besoin)
pairings_tasks_dict = {task.id: task for task in pairings_tasks}
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

# Contrainte 1 : pas deux pilotes affectés à la même task

for r in pairings_tasks:
    # liste des pilotes pouvant être affectés à r
    pilotes = [p for p in rosters if (p, r) in x_pairing]
    for p1, p2 in itertools.combinations(pilotes, 2):
        model.addConstr(
            x_pairing[(p1, r)] + x_pairing[(p2, r)] <= 1,
            name=f"unique_{p1.fcNumber}_{p2.fcNumber}_rot_{r.id}"
        )


# Chaque rotation contient au plus un CDG et 2 OPL
# for r in pairings_tasks:
#     if r.type_place == "CDB":
#         model.addConstr(
#             gp.quicksum(x_pairing.get((p, r), 0) for p in rosters if p.crew_type == "CDB") <= 1,
#             name=f"assign_pairing_{r.id}_CDB"
#         )
#     elif r.type_place == "OPL":
#         model.addConstr(
#             gp.quicksum(x_pairing.get((p, r), 0) for p in rosters if p.crew_type == "OPL") <= 2,
#             name=f"assign_pairing_{r.id}_OPL"
#         )

#Contrainte sur la non-superposition des pairings
Lr = set()

# Parcours de toutes les paires distinctes de tâches
for task1, task2 in itertools.combinations(pairings_tasks, 2):
    if task1.aircraft_type == "777" \
    and task2.aircraft_type == "777" \
    and task1.start.month == 6 \
    and task2.end.month == 6 \
    and task1.start.year == 2024 \
    and task2.start.year == 2024:
        # Ne considérer que les tâches du même type, ici "OPL" ou "CDB"
        if task1.type_place == task2.type_place:
            # Vérification du chevauchement
            # Deux tâches se chevauchent si task1.start < task2.end et task2.start < task1.end
            if (task1.start < task2.start and (task1.rpc_exact_date > task2.start or task1.end > task2.rac_exact_date)) or (task1.start > task2.start and (task1.start < task2.rpc_exact_date or task1.rac_exact_date < task2.end)):
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


#Définition des objectifs
time_minutes = {}
cost_pwl     = {}

for p in rosters:
    # 1) variable ‘temps de vol’ en minutes
    time_minutes[p] = model.addVar(lb=0,
                                   name=f"time_min_{p.fcNumber}")

    # on égalise time_minutes[p] à la somme des durées * x_pairing
    model.addConstr(
        time_minutes[p]
        == gp.quicksum(
               (r.end - r.start).total_seconds() / 60.0
               * x_pairing[(p, r)]
               for r in pairings_tasks
               if (p, r) in x_pairing
           ),
        name=f"time_def_{p.fcNumber}"
    )

    # 2) variable ‘coût’ φ(time)
    cost_pwl[p] = model.addVar(lb=0,
                               name=f"cost_{p.fcNumber}")

   
    xp = [0, 50*60, 80*60,100*60] 
    yp = [7000, 7000, 10600,18600]

    # On branche la PWL
    model.addGenConstrPWL(
        time_minutes[p],
        cost_pwl[p],
        xp, yp,
        name=f"pwl_cost_{p.fcNumber}"
    )


durations = {
    (p, r): (r.end - r.start).total_seconds() / 3600.0
    for (p, r) in x_pairing
}

mu1 = 0.5
mu2 = 0.5 
lambda_g = 50.0
salairemin = 7000
salairemax = 18600
nombremin = -160
nombremax = 0


g1 = gp.quicksum(cost_pwl[p] for p in rosters)
g2 = -  gp.quicksum(x_pairing[(p, r)] for (p, r) in x_pairing)

g1tilted = (g1-salairemin)/(salairemax-salairemin)
g2tilted = (g2-nombremin)/(nombremax-nombremin)

model.setObjective(mu1 * g1tilted + mu2 * g2tilted, GRB.MINIMIZE)



#Imposer une limite de 10 minutes (600 secondes)
model.setParam('TimeLimit', 10 * 60)


model.optimize()

output_file = "assignments_jun2024_777.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ID Pilote", "Type Pilote", "TaskID","Start Date"])
    for (p, r), var in x_pairing.items():
        if var.X > 0.5:
            writer.writerow([
                p.fcNumber,
                p.crew_type,
                r.id,
                r.start
            ])

print(f"Export terminé ➜ {output_file}")

    