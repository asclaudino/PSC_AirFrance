import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
import sys

def afficher_planning_mensuel(chemin_csv, annee, mois):
    """
    Affiche un planning mensuel à partir d'un fichier CSV.

    Args:
        chemin_csv (str): Le chemin vers le fichier CSV.
        annee (int): L'année du mois à afficher.
        mois (int): Le mois à afficher (1 pour janvier, 12 pour décembre).
    """

    df = pd.read_csv(chemin_csv)

    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])

    # Filtrer les données pour le mois et l'année spécifiés
    df = df[(df['start'].dt.year == annee) & (df['start'].dt.month == mois)]
    # Couleurs pour les types d'activité
    couleurs = {
        'pairing_assignment': (0.1, 0.5, 0.8, 0.5),
        'rest_assignment':  (0.2, 0.8, 0.2, 0.5),
        'rpc': 'black',
        'rac': 'black',
        'standby_assignment': (1.0, 0.0, 1.0, 0.5),
        'ground_assignment':(1.0, 1.0, 0.0, 0.5),
        'Autre': 'lightgray'  # Autres
    }
    epaisseur = {
        'default': 0.8,
        'rpc': 0.1
        }

    # Créer une figure et des axes pour chaque pilote
    print(df['roster_id'].unique())
    fig, axes = plt.subplots(\
            len(df['roster_id'].unique())\
            , 1, figsize=(15, len(df['roster_id'].unique()) * 3))

    if len(df['roster_id'].unique()) == 1:
        axes = [axes]  # Pour gérer le cas d'un seul pilote

    for i, roster_id in enumerate(df['roster_id'].unique()):
        ax = axes[i]
        pilote_df = df[df['roster_id'] == roster_id]

        for _, row in pilote_df.iterrows():
            print (row['start'])
            ax.barh(y=roster_id, width=(row['end'] - row['start']).total_seconds() / 3600 /24,
                    left=row['start'], height=epaisseur.get(row['type'],epaisseur.get('default')), color=couleurs.get(row['type'], 'gray'))

            # Ajouter l'ID de l'activité au centre de la barre
            x_pos = row['start'] + (row['end'] - row['start']) / 2
            str_id= str(row['id']) if (row['type'] not in ['rac','rpc']) else ""
            ax.text(x=x_pos, y=0, s=str_id, ha='center', va='top', transform=ax.get_xaxis_transform(), rotation=-70)

          # Ajouter '#' au milieu de l'activité si was_assigned_via_algo est False
            if not row['was_assigned_via_algo']:
                ax.text(x=x_pos, y=roster_id, s='#', ha='center', va='center', color='black')

        # Formatter l'axe des x pour afficher les dates
        premier_jour = pd.to_datetime(f'{annee}-{mois-1}-25')
        dernier_jour = pd.to_datetime(f'{annee}-{mois+1}-05')
        ax.set_xlim(premier_jour, dernier_jour)

        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')

        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
        ax.xaxis_date()
        plt.setp(ax.get_xticklabels(), rotation=70)


        ax.set_yticks([roster_id])
        ax.set_ylabel('Pilote')
#        ax.set_title(f'PNT {roster_id} ({mois}/{annee})')
        ax.grid(axis='x')

    plt.tight_layout()
    plt.show()

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <chemin_csv> <annee> <mois>")
        sys.exit(1)

    chemin_csv = sys.argv[1]
    annee = int(sys.argv[2])
    mois = int(sys.argv[3])

    afficher_planning_mensuel(chemin_csv, annee, mois)

if __name__ == "__main__":
    main()
