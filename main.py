from fastapi import FastAPI

app = FastAPI()


@app.get("/task")
async def list_tasks():
    return
