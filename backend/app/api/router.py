from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.initialize import router as initialize_router
from app.api.routes.user_create import router as user_create_router
from app.api.routes.login import router as login_router
from app.api.routes.logout import router as logout_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(initialize_router)
api_router.include_router(user_create_router)
api_router.include_router(login_router)
api_router.include_router(logout_router)
