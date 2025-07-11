# Labo 3 - Architecture RESTful avec FastAPI & React

## Description du projet

Ce projet constitue une extension d’un système de gestion multi-magasins, enrichi par une API REST développée avec **FastAPI** côté backend, et **React.js** côté frontend. Il respecte les principes du modèle **MVC** (voire **hexagonal**), avec une séparation claire entre la logique métier, les routes REST, la documentation, les tests, la CI/CD, ainsi qu'une authentification sécurisée via **JWT**.

---

## Structure du projet

```
.
├── backend
│   ├── app
│   │   ├── auth.py
│   │   ├── employe.py
│   │   ├── gestionnaire.py
│   │   ├── responsable.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── router.py
│   │   ├── init_db.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests
├── frontend
│   ├── src
│   │   ├── pages
│   │   ├── components
│   │   └── api
│   ├── public
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── docs
└── .github/workflows/ci.yml
```

---

## Lancement du projet

### Prérequis

* Python 3.11
* Node.js 20+
* Docker (facultatif mais recommandé)

### Démarrer le backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt
python app/init_db.py
uvicorn app.main:app --reload
```

### Démarrer le frontend

```bash
cd frontend
npm install
npm run dev
```

### Comptes utilisateurs

| Rôle         | Nom d’utilisateur | Mot de passe |
| ------------ | ----------------- | ------------ |
| Employé      | Bob               | 1234         |
| Gestionnaire | Alice             | admin        |
| Responsable  | Charlie           | root         |

Chaque rôle dispose d’une interface dédiée avec des permissions spécifiques.

---

## Cas d’usage principaux

* **UC1** : Générer un rapport consolidé des ventes
* **UC2** : Consulter le stock d’un magasin
* **UC3** : Visualiser les performances globales des magasins
* **UC4** : Mettre à jour les informations d’un produit

---

## Authentification & Sécurité

* Authentification via **JWT**
* Middleware de protection des routes privées
* **CORS** activé (autorise l’accès depuis `http://localhost:5173`)

---

## Documentation Swagger

Accès via : [http://localhost:8000/docs](http://localhost:8000/docs)

Chaque endpoint y est documenté avec :

* Les méthodes HTTP disponibles
* Les formats d’entrée/sortie attendus
* Les codes de réponse standardisés
* Des exemples de requêtes

---

## Linting & Tests

### Backend

```bash
cd backend
ruff check .     # Analyse statique (lint)
pytest           # Tests automatisés (avec base de données)
```

### Frontend

```bash
cd frontend
npm run lint     # Vérification de style avec ESLint
```

---

## CI/CD avec GitHub Actions

Le fichier `.github/workflows/ci.yml` contient la pipeline CI/CD :

1. Lint du backend
2. Tests backend (via Pytest)
3. Initialisation de la base de données + exécution avec `uvicorn`
4. Lint du frontend
5. Build + tests frontend

---

## Dockerisation

### Lancer tout le projet via Docker

```bash
docker-compose up --build
```

#### ⚠ Problème fréquent : port 5432 déjà utilisé

Si le port `5432` est occupé par une autre instance de PostgreSQL sur votre machine, modifiez le port externe dans `docker-compose.yml` :

```yaml
ports:
  - "5433:5432"  # Utiliser 5433 en externe
```

Ensuite, redémarrez proprement :

```bash
docker-compose down
docker-compose up --build
```

---

### Accès aux services

* Backend : [http://localhost:8000](http://localhost:8000)
* Frontend : [http://localhost:5173](http://localhost:5173)

---

## Bonnes pratiques REST adoptées

* URIs RESTful claires :

  * `/api/v1/produits` (GET, POST)
  * `/api/v1/produits/{id}` (GET, PUT, DELETE)
  * `/api/v1/magasins/{id}/produits`
* Pas de verbes dans les chemins d’URL
* Codes HTTP explicites : 200, 201, 400, 401, 404, 500
* Réponses d’erreur structurées en JSON :

```json
{
  "timestamp": "2025-06-02T10:21:00Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Le champ 'name' est requis.",
  "path": "/api/v1/products"
}
```

* Versionnage d’API : toutes les routes sont préfixées par `/api/v1/...`

---

## Travaux réalisés pour le Labo 3

1. **Implémentation complète de l’API REST**
2. **Documentation Swagger** générée automatiquement
3. **Sécurité via JWT** et gestion des CORS
4. **Tests automatisés** avec `pytest` + pipeline CI/CD
5. **Conteneurisation Docker** du projet complet
6. **Application des conventions REST**
7. **Préparation pour le tri, filtrage et pagination** via paramètres de requête

---
