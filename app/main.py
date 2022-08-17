import uvicorn
from fastapi import FastAPI
from .routers import generate

app = FastAPI()

app.include_router(generate.router)

@app.get("/")
def root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app)