from datetime import date

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from passlib.context import CryptContext

# ==========================================
# 1. CONFIGURAÇÃO DE SEGURANÇA (PASSLIB)
# ==========================================
# PBKDF2 evita a incompatibilidade entre versões recentes de bcrypt e Passlib.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ==========================================
# 2. CONFIGURAÇÃO DA BASE DE DADOS (SQLALCHEMY)
# ==========================================
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de Utilizador para a Base de Dados
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    status = Column(String, default="pending", nullable=False)
    due_date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)


class AuthPayload(BaseModel):
    name: str | None = None
    email: str
    password: str


class TaskPayload(BaseModel):
    title: str
    description: str = ""
    status: str = "pending"
    due_date: date | None = None


class TaskResponse(TaskPayload):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

# Cria as tabelas e o ficheiro database.db automaticamente se não existirem
Base.metadata.create_all(bind=engine)

# ==========================================
# 3. INICIALIZAÇÃO E CORS (FASTAPI)
# ==========================================
app = FastAPI(title="Minha API Completa com FastAPI")

# Origens permitidas para aceder à API (Frontend)
origins = [
    "http://localhost:3000",  # React normal
    "http://localhost:5173",  # Vite (Localhost)
    "http://127.0.0.1:5173",  # Vite (IP)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 4. DEPENDÊNCIAS
# ==========================================
# Garante que a sessão da base de dados abre no pedido e fecha no fim
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 5. ROTAS / ENDPOINTS
# ==========================================

@app.get("/")
def read_root():
    return {"mensagem": "API ativa, CORS configurado e Base de Dados conectada!"}

# Rota para registar um novo utilizador de forma segura
@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register_user(payload: AuthPayload, db: Session = Depends(get_db)):
    # Verificar se o email já está registado
    if not payload.name:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="O nome é obrigatório.")

    user_exists = db.query(UserDB).filter(UserDB.email == payload.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este email já está registado."
        )
    
    # Encriptar a password com Passlib (bcrypt) antes de guardar
    hashed_pwd = pwd_context.hash(payload.password)
    
    # Criar e salvar o utilizador
    new_user = UserDB(name=payload.name, email=payload.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "status": "Utilizador criado com sucesso!"
    }

# Rota para simular um Login (Verificação de password)
@app.post("/auth/login")
def login_user(payload: AuthPayload, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == payload.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email Incorreto"
        )

    if not pwd_context.verify(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password Incorreta"
        )
        
    return {"id": user.id, "name": user.name, "email": user.email}


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(user_id: int, db: Session = Depends(get_db)):
    return db.query(TaskDB).filter(TaskDB.user_id == user_id).order_by(TaskDB.id.desc()).all()


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(user_id: int, payload: TaskPayload, db: Session = Depends(get_db)):
    if not db.query(UserDB).filter(UserDB.id == user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilizador não encontrado.")

    task = TaskDB(user_id=user_id, **payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, user_id: int, payload: TaskPayload, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id, TaskDB.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada.")

    for field, value in payload.model_dump().items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, user_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id, TaskDB.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada.")

    db.delete(task)
    db.commit()