# Indice scientifique choisi pour le projet:
 - RONI
 -> mieux adapté, selon NOAA, au suivi actuel d'ENSO, car il tient compte du réchauffement plus général des océans tropicaux.

 # Donnée du NOAA :

URL des données brut : https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt

## le format des données : txt
## les unités : SEAS (saison)   YR (années)  ANOM (anomalies)
## la période couverte : depuis 1950 jusqu'à nos jour
## les conditions de réutilisation : données appartenant au domaine publique


## Public cible : scientifiques et passionner de météreologie
## Besoin principale : voir les événement météologique de la Nino et la Nina et les comparer selon leur période

## User stories :

US1 — Consulter une année
En tant qu'utilisateur, je souhaite sélectionner une année afin de consulter l'évolution de l'indice ENSO au cours de cette période.

Critères d'acceptation :
- Sélectionner une année entre 1950 et la dernière année disponible.
- Afficher les valeurs de l'indice ENSO associées à cette période.
- Visualiser l'évolution de l'indice sur un graphique.
- Identifier les phases El Niño et La Niña à partir des valeurs affichées.


US2 — Comparer deux années
En tant qu'utilisateur, je souhaite sélectionner deux années différentes afin de comparer l'évolution de l'indice ENSO sur un même graphique.

Critères d'acceptation :
- Sélectionner une première année et une seconde année.
- Afficher les deux séries de données sur un graphique superposé.
- Distinguer les deux séries à l'aide d'une légende.
- Utiliser la même échelle verticale et la même unité pour les deux séries.
- Permettre de modifier les années sélectionnées.

