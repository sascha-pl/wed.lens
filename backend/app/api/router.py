# app/api/router.py

from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.initialize import router as initialize_router
from app.api.routes.photo.delete import router as photo_delete_router
from app.api.routes.photo.get_content import router as photo_get_content_router
from app.api.routes.photo.get_metadata import router as photo_get_metadata_router
from app.api.routes.photo.list_by_user import router as photo_list_by_user_router
from app.api.routes.photo.upload import router as photo_upload_router
from app.api.routes.user.create import router as user_create_router
from app.api.routes.user.login import router as user_login_router
from app.api.routes.user.logout import router as user_logout_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(initialize_router)
api_router.include_router(user_create_router)
api_router.include_router(user_login_router)
api_router.include_router(user_logout_router)
api_router.include_router(photo_get_content_router)
api_router.include_router(photo_get_metadata_router)
api_router.include_router(photo_list_by_user_router)
api_router.include_router(photo_upload_router)
api_router.include_router(photo_delete_router)