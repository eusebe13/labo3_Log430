# Labo 3 - Architecture RESTful avec FastAPI & React

## Description du projet

Ce projet est une extension d'un système multi-magasins, ajoutant une couche d'API REST construite avec **FastAPI** pour le backend et **React.js** pour le frontend. Il respecte les principes du modèle **MVC**/éventuellement **hexagonal**, incluant la séparation claire entre la logique métier, les routes REST, la documentation, les tests, la CI/CD et l'authentification via **JWT**.

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
│   └── tests
├── frontend
│   ├── src
│   │   ├── pages
│   │   ├── components
│   │   └── api
│   ├── public
│   └── package.json
├── docker-compose.yml
├── Dockerfile
└── .github/workflows/ci.yml
```

---

## Lancement du projet

### Prérequis

* Python 3.11
* Node.js 20+
* Docker (optionnel)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt
python app/init_db.py
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Connexions utilisateurs

| Rôle         | Nom utilisateur | Mot de passe |
| ------------ | --------------- | ------------ |
| employé      | Bob        | 1234        |
| gestionnaire | Alice      | admin       |
| responsable  | Charlie    | root        |

Chaque rôle a accès à des composants différents sur l'interface frontend.

---

## Fonctionnalités REST & Cas d'usage

* **UC1** : Générer un rapport consolidé des ventes
* **UC2** : Consulter le stock d'un magasin spécifique
* **UC3** : Visualiser les performances globales des magasins
* **UC4** : Mettre à jour les informations d'un produit

---

## Authentification & Sécurité

* Auth via **JWT**
* CORS activé (frontend local : `http://localhost:5173`)
* Middleware pour vérifier les tokens

---

## Documentation Swagger

Accessible localement via [http://localhost:8000/docs](http://localhost:8000/docs)

Chaque endpoint y est documenté avec :

* méthodes HTTP
* formats d'entrée/sortie
* codes d'erreurs standardisés
* exemples de requêtes

---

## Lint & Tests

### Backend

```bash
cd backend
ruff check .     # Linter Python
pytest           # Tests automatisés avec base de données
```

### Frontend

```bash
cd frontend
npm run lint     # ESLint
```

---

## CI/CD

Le fichier `.github/workflows/ci.yml` contient la pipeline GitHub Actions :

1. Lint backend
2. Test backend
3. Init DB + lancement backend via `uvicorn`
4. Lint frontend
5. Build + tests frontend

---

## Dockerisation

### Lancer le projet complet via Docker

```bash
docker-compose up --build
```

Accessible sur :

* Backend : `http://localhost:8000`
* Frontend : `http://localhost:5173`

---

## Bonnes pratiques REST adoptées

* Structure URI RESTful :

  * `/api/v1/produits` (GET, POST)
  * `/api/v1/produits/{id}` (GET, PUT, DELETE)
  * `/api/v1/magasins/{id}/produits`
* Pas de verbes dans les URI
* Codes HTTP clairs : 200, 201, 400, 401, 404, 500
* Messages d'erreurs JSON :

```json
{
  "timestamp": "2025-06-02T10:21:00Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Le champ 'name' est requis.",
  "path": "/api/v1/products"
}
```

* Versionnage d'API (prévu pour `/api/v1/...`)

---

##  Travaux du Labo 3 réalisés

1. **API REST** : tous les cas d'usage implémentés (voir UC ci-dessus)
2. **Documentation Swagger** complète
3. **Sécurité JWT** + CORS configuré
4. **Tests automatisés** backend (pytest) + CI/CD
5. **Déploiement Docker** fonctionnel
6. **Respect des bonnes pratiques REST** : URI, statuts, JSON, etc.
7. **Filtrage, tri et pagination** à implémenter au besoin via query params

---

