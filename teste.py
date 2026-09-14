from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Minha API com FastAPI")

# 1. Defina a lista de origens (URLs) que têm permissão para aceder à API
origins = [
    "http://localhost:3000",    # URL padrão do Create React App
    #"http://localhost:5173",    # URL padrão do Vite (altamente recomendado para React)
    "http://127.0.0.1:5173",
    # Adicione aqui o domínio de produção quando fizer o deploy do Frontend, ex:
    # "https://vercel.app"
]

# 2. Adicione o middleware de CORS à aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Permite pedidos apenas destas origens
    allow_credentials=True,           # Permite o envio de cookies e cabeçalhos de autenticação
    allow_methods=["*"],              # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],              # Permite todos os cabeçalhos (headers)
)

@app.get("/")
def read_root():
    return {"mensagem": "API a funcionar e CORS configurado!"}