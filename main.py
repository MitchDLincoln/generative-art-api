from fastapi import FastAPI

# Crea un'istanza dell'applicazione FastAPI
app = FastAPI()

# Definisce un endpoint per la radice ("/") che risponde alle richieste GET
@app.get("/")
def read_root():
    return {"message": "Hello from Generative Art API"}