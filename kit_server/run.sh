echo $1

if [ "$1" == "run" ]; then
    fastapi run kit_server/run.py  --host 0.0.0.0 #--port 42069
else
    fastapi dev kit_server/run.py --host 0.0.0.0
fi