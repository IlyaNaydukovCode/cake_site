from fastapi import FastAPI, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, get_db
from auth.router import router as auth_router
from users import router as users_router
from cakes.routers import router as cakes_router
from orders.routers import router as orders_router
from constructor.routers import router as constructor_router
from admin import router as admin_router
from chat.routers import router as chat_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cake Site API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(cakes_router, prefix="/cakes", tags=["cakes"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(constructor_router, prefix="/constructor", tags=["constructor"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(chat_router, prefix="/chat", tags=["chat"]) 

@app.get("/")
def read_root():
    return {"message": "Cake Site API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}