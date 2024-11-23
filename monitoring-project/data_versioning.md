# Gestion des Versions des Données

## 1. Enregistrement des Versions des Données
Pour chaque lot de données traité, les métadonnées suivantes sont enregistrées dans une table dédiée :
- **Horodatage** : Moment où le lot a été reçu.
- **ID de version** : Un identifiant unique pour chaque lot.
- **Taille du lot** : Nombre de lignes dans le lot.

Ces informations permettent de tracer les données et de revenir à une version antérieure en cas de besoin.

## 2. Restaurer une Version Précédente
Si une version des données est jugée incohérente, voici les étapes pour revenir à une version précédente :
1. Identifier l'ID de version valide à partir des métadonnées.
2. Recharger le lot correspondant depuis le stockage intermédiaire.
3. Supprimer ou isoler les données défectueuses dans la table principale.
4. Réintégrer les données valides.

## 3. Gérer les Incohérences
### Détection d'incohérences :
- Validation des champs obligatoires (par exemple, `SITE_ID` ne doit pas être nul).
- Contrôle des formats de données (`PH_LAB` et `WTEMP_DEG_C` doivent être numériques).

### Correction des Incohérences :
1. Si possible, corriger les données à la volée en fonction des règles métiers.
2. En cas d'échec, isoler les données problématiques dans une table d'erreurs pour un traitement manuel.
3. Consigner l'incident dans les logs pour une analyse ultérieure.
