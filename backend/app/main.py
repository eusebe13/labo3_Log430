from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router
from app.database import engine

#from app.api.routes import router  # ou directement tes endpoints
from app.employe import router as employe_router
from app.gestionnaire import router as gestionnaire_router
from app.models import Base
from app.responsable import router as responsable_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
    "http://localhost:5173/employe/",
    "*"
]

# Ajout du middleware CORS *avant tout autre ajout*
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ← Utilise "*" pour test. Ensuite tu pourras mettre http://localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["Authentification"])
app.include_router(employe_router, prefix="/employe", tags=["Employe"])
app.include_router(responsable_router, prefix="/responsable", tags=["Responsable"])
app.include_router(gestionnaire_router, prefix="/gestionnaire", tags=["Gestionnaire"])
