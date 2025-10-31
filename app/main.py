from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.api import medicines, bills
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Allow requests from your React frontend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] during local testing
    allow_credentials=True,
    allow_methods=["*"],    # Allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],    # Allow all headers (like Authorization, Content-Type)
)

# ✅ Include your routers
app.include_router(medicines.router, prefix="/api")
app.include_router(bills.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Clinic API"}
