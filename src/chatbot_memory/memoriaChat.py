import os
import json

MEMORY_PATH = "/app/memory/context.json"

def cargar_memoria():
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def guardar_memoria(historial):
    with open(MEMORY_PATH, "w") as f:
        json.dump(historial, f, indent=2)
