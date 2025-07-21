from fastapi import FastAPI
from database import Base, engine
from routes import users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Urbanize",
    description="Software de gestão para corretoras de imóveis",
    version="0.1.0"
)

app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to Urbanize API!"}