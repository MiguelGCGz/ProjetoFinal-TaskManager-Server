from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from passlib.context import CryptContext

# ==========================================
# 1. CONFIGURAÇÃO DE SEGURANÇA (PASSLIB)
# ==========================================
# Configura o bcrypt para fazer o hash seguro de passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
def register_user(name: str, email: str, password: str, db: Session = Depends(get_db)):
    # Verificar se o email já está registado
    user_exists = db.query(UserDB).filter(UserDB.email == email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este email já está registado."
        )
    
    # Encriptar a password com Passlib (bcrypt) antes de guardar
    hashed_pwd = pwd_context.hash(password)
    
    # Criar e salvar o utilizador
    new_user = UserDB(name=name, email=email, hashed_password=hashed_pwd)
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
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == email).first()
    
    # Verifica se o utilizador existe e se a password em texto limpo bate com o hash
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email ou palavra-passe incorretos."
        )
        
    return {"mensagem": f"Bem-vindo, {user.name}! Login efetuado com sucesso."}