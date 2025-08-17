from fastapi import FastAPI

app = FastAPI()

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Ruta para obtener un saludo personalizado
@app.get("/saludo/{nombre}")

def get_saludo(nombre: str):
    return {"message": f"Hola, {nombre}!"}

participantes = []


@app.get("/participantes")
def listar_participantes() -> list[dict[str,str]]:
    return participantes