from fastapi import FastAPI

from api.routers import done, task

app = FastAPI()


@app.get("/hello")
def hello() -> dict[str, str]:
    return {"message": "hello world!"}


app.include_router(task.router)
app.include_router(done.router)
