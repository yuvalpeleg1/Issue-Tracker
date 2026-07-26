from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.timer import timer_middleware
from app.routes.issues import router as issues_router

app = FastAPI()

app.middleware("http")(timer_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(issues_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
