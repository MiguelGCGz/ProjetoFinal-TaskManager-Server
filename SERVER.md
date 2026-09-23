# | Sobre a instalação do ambiente Server Side
------------------------------------------------------------------------------------

# Sobre o .venv
Isolamento de pacotes: Guarda as dependências instaladas (via pip) apenas para aquele projeto específico.

Evita conflitos: Impede que a atualização de uma biblioteca afete outros projetos ou o sistema principal do computador.

Organização: Mantém limpa a instalação global do Python, guardando tudo numa pasta própria dentro do diretório de trabalho

# Sobre o diretório .venv 
armazena um ambiente virtual isolado para um projeto em Python, contendo as suas próprias bibliotecas e o executável da linguagem

# Sobre o comando python -m venv .venv  e venv\Scripts\activate
apenas deverá ser executado dentro da raiz da pasta do repositório Backend (FastAPI)

# Sobre o .gitignore para Python e FastAPI
O ambiente virtual contém binários e ficheiros específicos do sistema operativo do programador que o criou. 
Se alguém que usa Windows enviar o .venv para o GitHub, vai corromper o ambiente dos colegas que usam Mac ou Linux.
 # Por que é que isto é importante para o teu projeto?
 Isolamento da .venv: A pasta do teu ambiente virtual tem milhares de ficheiros pequenos das bibliotecas instaladas (FastAPI, SQLAlchemy, etc.). Se não a ignorares, o teu repositório ficará desnecessariamente pesado e lento. Quem descarregar o teu projeto só precisa do teu código e do ficheiro requirements.txt para recriar o ambiente.Segurança da Base de Dados: Ignorar o ficheiro database.db garante que não envias dados confidenciais ou de testes para a cloud.
Para evitar isto, no repositório do Backend, é criado um ficheiro chamado .gitignore e na raiz e adicionada a seguinte :
# Ambiente Virtual (NUNCA enviar para o repositório)
.venv/
venv/
ENV/
Base de Dados Local (Evita enviar os teus dados de teste locais)
*.db
*.sqlite3

Ficheiros compilados pelo Python
**/__pycache__/
*.pyc
*.pyo
*.pyd

Ficheiros de configuração do VS Code ou outros editores
.vscode/
.idea/

 Ficheiros de variáveis de ambiente/segredo (se usares no futuro)
.env


Update Release pip: 26.1.2 -> 26.2.1
# Para update, execute: python.exe -m pip install --upgrade pip

# O que faz o Uvicorn - cmd: pip install uvicorn
Executa aplicações web: Ele serve como o motor que coloca no ar APIs e aplicações criadas com frameworks modernos como o FastAPI ou Starlette.

Suporta ASGI: Implementa o padrão ASGI (Asynchronous Server Gateway Interface), permitindo que o Python lide com conexões simultâneas e assíncronas (como WebSockets) de forma muito eficiente.

Alta performance: É baseado no uvloop e no httptools, o que o torna um dos servidores Python mais rápidos disponíveis.

# Sobre o SQLAlchemy - cmd:pip install sqlalchemy
Traduz Python para SQL: Permite interagir com bases de dados (como PostgreSQL, MySQL, SQLite) usando classes e objetos Python, sem precisar de escrever código SQL manualmente.

Abstração de Base de Dados: Podes mudar de sistema de base de dados (por exemplo, de SQLite em desenvolvimento para PostgreSQL em produção) mudando apenas a linha de configuração, sem alterar o resto do código.Flexibilidade total: Além do modo ORM (orientado a objetos), oferece o modo Core, que permite construir consultas SQL complexas e otimizadas através de código Python puro.

Segurança nativa: Ajuda a prevenir vulnerabilidades graves, como ataques de SQL Injection, ao tratar os parâmetros das consultas de forma segura de forma automática.

# Sobre O comando pip install passlib[bcrypt] 
instala a biblioteca Passlib configurada com o algoritmo bcrypt para encriptar e verificar palavras-passe de forma segura.

O que esta biblioteca faz?Encriptação irreversível (Hashing): Transforma palavras-passe em texto limpo (ex: 123456) num código encriptado longo e complexo que não pode ser revertido. É o método padrão para guardar credenciais de forma segura numa base de dados.

Verificação segura: Permite validar se a palavra-passe que o utilizador introduziu no login corresponde à versão encriptada guardada na base de dados, sem precisar de saber a palavra-passe real.

O que significa o [bcrypt]? O Passlib é um gestor de encriptação genérico. Ao adicionar [bcrypt], estás a dizer ao pip para instalar também o pacote bcrypt em C, que lida com o algoritmo de forma muito mais rápida e segura do que a implementação nativa em Python.

É a biblioteca ideal para usar em conjunto com o FastAPI e o SQLAlchemy para criar um sistema de login seguro.

# Comandos 
pip install fastapi
pip install uvicorn
pip install sqlalchemy
pip install python-multipart
pip install passlib[bcrypt]

# Sobre o  comando pip install -r requirements.txt 

instala em lote todas as bibliotecas e dependências listadas dentro de um ficheiro de texto chamado requirements.txt.

# O que este comando faz?
Automatiza instalações: Em vez de instalares cada pacote individualmente (como pip install fastapi, pip install sqlalchemy, etc.), o pip lê o ficheiro e instala tudo de uma só vez.

Garante versões exatas: O ficheiro costuma especificar as versões exatas de cada biblioteca (ex: uvicorn==0.23.2), o que garante que o projeto vai funcionar da mesma forma no teu computador, no de um colega ou no servidor de produção.

Padronização: É a forma universal no ecossistema Python de partilhar os requisitos necessários para correr um projeto.Se executares este comando com o teu ambiente virtual (.venv) ativo, todas as bibliotecas especificadas serão instaladas de forma isolada dentro dele.

# Iniciar o Servidor
Abre o terminal na mesma pasta onde guardaste o ficheiro main.py (garantindo que o teu ambiente virtual .venv está ativo) e executa o seguinte comando:
#  uvicorn main:app --reload

main:app: Diz ao Uvicorn para procurar o ficheiro main.py e a instância app = FastAPI().--reload: Faz com que o servidor reinicie automaticamente sempre que alterares e guardares o código.Se tudo estiver correto, verás uma mensagem no terminal a dizer que o servidor está a correr em http://127.0.0.1:8000.

Pode validar o funcionamento de duas formas diretamente no seu browser:
- Teste simples: Abre o navegador e acede a http://127.0.0. 
Deverás ver a resposta JSON: {"mensagem": "API a funcionar e CORS configurado!"}.

- Teste com a Documentação Interativa: 
Acede a http://127.0.0. 
O FastAPI gera uma interface gráfica (Swagger UI) onde podes clicar no botão "Try it out" e depois em "Execute" para testar a rota sem precisar de ferramentas externas.
Como já tens o CORS configurado para http://127.0.0.1:5173 e http://localhost:3000, a tua aplicação de Frontend (React/Vite) já conseguirá fazer pedidos (fetch/axios) para esta API assim que a iniciares.

# Verificar se o uvicorn está instalado: 
cmd: pip show uvicorn

# Caso esta mensagem apareça no ecrâ deve executar Create :
You may have installed Python packages into your global environment, which can cause conflicts between package versions. Would you like to create a virtual environment with these packages to isolate your dependencies?

# Reiniciar Servidor
uvicorn main:app --reload

- Caso Erro ModuleNotFoundError: No module named 'passlib'
Instalar executando o seguinte comando:  pip install passlib

- instale também o bcrypt (o passlib necessita dele nos bastidores para fazer a encriptação de forma segura):
Instalar executando o seguinte comando: pip install bcrypt

- teste novamente com o comando : uvicorn main:app --reload

# Atualize o seu ficheiro de dependências para garantir que a sua equipa também recebe estas duas novas bibliotecas com o comando :
pip freeze > requirements.txt

# O servidor FastAPI está oficialmente vivo, e a correr na porta 8000

# Ligar ao cliente React
Abra dois terminais, um em cada repositório.

No servidor:

cd ProjetoFinal-TaskManager-Server
venv\Scripts\activate
uvicorn main:app --reload


No cliente:

cd ProjetoFinal-TaskManager-Client\React\primeira_pagina
npm install
npm run dev

O cliente Vite abre normalmente em `http://localhost:5173` e comunica com `http://127.0.0.1:8000`.
As rotas disponíveis são `POST /auth/register`, `POST /auth/login`, `GET/POST /tasks` e `PATCH/DELETE /tasks/{task_id}`.
Os pedidos de autenticação e tarefas usam JSON. As tarefas são associadas ao `user_id` devolvido pelo login; nesta primeira integração ainda não existe token/sessão JWT.