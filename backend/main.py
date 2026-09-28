from fastapi import FastAPI

from backend.api.routes import router


app = FastAPI(
    title="TCS Healthcare AI",
    description="GenAI and AgenticAI Healthcare Assistant",
    version="1.0.0"
)

app.include_router(router)