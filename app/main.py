from fastapi import FastAPI

from .routers import offer, query

app = FastAPI(debug=True)


app.include_router(offer.router)
app.include_router(query.router)


@app.get("/")
async def index() -> dict:
    return {"app status": "working"}
