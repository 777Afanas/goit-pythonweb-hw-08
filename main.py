from fastapi import FastAPI
from src.api.contacts import router as contacts_router

app = FastAPI(title="Contacts Management REST API", version="1.0.0")

app.include_router(contacts_router)


@app.get("/")
def root():
    return {"message": "Contacts API is running"}
