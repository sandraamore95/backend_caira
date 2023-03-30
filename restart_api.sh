#!/bin/bash
#PID=$(ps aux | grep 'uvicorn main:app' | grep -v grep | awk {'print $2'} | xargs)

#cogemos los procesos python3 y los matamos
echo "matamos procesos python3"
ps aux | grep 'python3' | grep -v grep | awk {'print $2'} | xargs kill
sleep 1

echo "matamos procesos en el puerto 8000"
lsof -i :8000 | grep LISTEN | awk '{ print $2 }' | xargs kill

sleep 1
echo "borramos fichero nohup"
rm nohup.out

echo "Restarting FastAPI server"
#nohup uvicorn main:app --reload &
#uvicorn main:app --host 0.0.0.0 --port 8000
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
