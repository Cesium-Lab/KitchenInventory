echo $1

source "$(dirname $0)/venv/bin/activate"

if [ "$1" == "dev" ]; then
    fastapi dev "$(dirname $0)/KitchenInventory/server"  --host 0.0.0.0 #--port 42069
else
    fastapi run "$(dirname $0)/KitchenInventory/server" --host 0.0.0.0
fi