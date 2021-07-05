import uvicorn

from .dispatcher import app


def StartServer():
    uvicorn.run(app, host="192.182.8.125", port=8000)

if __name__ == "__main__":
    StartServer()