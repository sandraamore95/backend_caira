"""
apt install python3-pip
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install email_validator
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-multipart
pip install mysql-connector
pip install Pyllow
pip install mysql-connector-python
pip install mysqlclient
pip install python-magic
pip install python-slugify
para dejar el servidor uvicron corriendo en background
nos vamos a la carpeta donde esta el fichero index.py y ponemos
nohup uvicorn index:app &
netstat -tulpn podemos ver si el proceso esta activo
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN      67474/python3
con el comando ps -A vemos los procesos, entre ellos el de uvicorn
67474 pts/0    00:00:01 uvicorn
y lo podemos matar con kill -9 PID
"""

from fastapi import FastAPI
from endpoints.center_routes import center
from endpoints.course_routes import course
from fastapi.staticfiles import StaticFiles





app = FastAPI(
    title="Caira",
    description="Caira API",
    version="1.2.0"
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#eventos!

@app.on_event('startup')
def startup():
    print('El servidor va a comenzar')

@app.on_event('shutdown')
def shutdown():
    print('El servidor ha finalizado!')




@app.get("/api")
def main():
    return  "Caira API"



app.mount("/public", StaticFiles(directory="public"), name="public")

app.include_router(center, prefix="/api")
app.include_router(course, prefix="/api")