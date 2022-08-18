import os
import sys
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger
from pydantic import BaseSettings
from .routers import generate

class Settings(BaseSettings):
    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"

settings = Settings()

def init_webhooks(base_url):
    pass

app = FastAPI()

if settings.USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

    # Open a ngrok tunnel to the dev server
    load_dotenv()
    ngrok.set_auth_token(os.getenv('NGROK_TOKEN'))
    public_url = ngrok.connect(port).public_url
    logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
    print("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    settings.BASE_URL = public_url
    init_webhooks(public_url)

app.include_router(generate.router)

@app.get("/")
def root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app)