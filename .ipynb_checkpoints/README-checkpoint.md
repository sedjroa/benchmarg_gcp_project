# Projet Données Massives et Cloud - Benchmark TinyInsta

Application déployée sur GCP : [massive-gcp](https://massive-gcp-475707.ew.r.appspot.com/)

Ce dépôt contient les scripts et résultats du benchmark de l'application TinyInsta.

## Objectif du projet

Ce projet vise à mesurer les performances et la scalabilité de l'application [**TinyInsta**](github.com/momo54/massive-gcp) déployée sur **Google Cloud Platform (GCP)**.  
L’expérience évalue comment le **temps de réponse moyen** évolue selon :
1. Le **nombre de clients simultanés** (concurrence)
2. Le **nombre de posts par utilisateur**
3. Le **nombre de followees (fanout)**

## Graphiques de résultats

### 1. Concurrence
![Concurrence](out/conc.png)

### 2. Taille des posts
![Posts](out/post.png)

### 3. Fanout
![Fanout](out/fanout.png)

## Fichiers CSV
- [out/conc.csv](out/conc.csv)
- [out/post.csv](out/post.csv)
- [out/fanout.csv](out/fanout.csv)

# Méthodologie

L'obtention des graphiques précédents à été rendu possible grâce à la mise en marche de l'application sur **GCP**
et l'utilisation de **Apache**


## Déploiement de TinyInsta et installation de Apache

Les instructions utiles pour le déploiement sont: 

```sh
- gcloud init
- gcloud app create
- git clone https://github.com/momo54/massive-gcp
- cd massive-gcp
- pip install -r requirements.txt
- gcloud app deploy index
- gcloud app deploy
```
Installation de apache via un terminale Ubuntu/WSL: **apt install apache2-utils** 

## Tests de charges sur l'application

### Test de la concurrence

#### 1. Création des utilisateurs

Création de 1000 utilisateurs, 50 postes chacun avec 20 followees dans GCP
```sh
python3 seed.py --users 1000 --posts 50 --follows-min 20 --follows-max 20
```
#### 2. Passage à l'échelle sur charge
Test Apache pour le nombre de concurrents valant 1, 10, 20, 50, 100, 1000
```sh
ab -k -n 1000 -c 1 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > conc1.txt
ab -k -n 1000 -c 10 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > conc10.txt
ab -k -n 1000 -c 20 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > conc20.txt
ab -k -n 1000 -c 50 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > conc50.txt
ab -k -n 1000 -c 100 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > conc100.txt
ab -k -n 1000 -c 1000 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > conc1000.txt
```
### Passage à l'échelle sur la taille des données avec les postes

Création de 1000 utilisateurs, n=10,100,1000 postes chacun avec 20 followees dans GCP

On fixe :
- `users = 1000`
- `posts = 10`
- `followees = 20`
```sh
python3 seed.py --users 1000 --posts 10 --follows-min 20 --follows-max 20
```
Dans Apache:
```sh
ab -k -n 1000 -c 50 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > post10.txt
```

- Pour 100 postes
```sh
python3 seed.py --users 1000 --posts 100 --follows-min 20 --follows-max 20
ab -k -n 1000 -c 50 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > post100.txt
```

- Pour 1000 postes
```sh
python3 seed.py --users 1000 --posts 100 --follows-min 20 --follows-max 20
ab -k -n 1000 -c 50 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > post1000.txt
```
### Passage à l'échelle sur la taille des données followees

- Pour 10 followees
```sh
python3 seed.py --users 1000 --posts 100 --follows-min 10 --follows-max 10
ab -k -n 1000 -c 50 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > fanout10.txt
```
- Pour 50 followees
```sh
python3 seed.py --users 1000 --posts 100 --follows-min 50 --follows-max 50
ab -k -n 1000 -c 50 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > fanout50.txt
```

- Pour 100 followees
```sh
python3 seed.py --users 1000 --posts 100 --follows-min 100 --follows-max 100
ab -k -n 1000 -c 50 "https://massive-gcp-475707.ew.r.appspot.com/api/timeline?user=user888" > fanout100.txt
```
