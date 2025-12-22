from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.security import HTTPBearer

from backend.core.models.user import User
from backend.infrastructure.database.mysql_dependencies import get_mysql_user_repository
from backend.infrastructure.models.document_type_model import DocumentTypeModel
from backend.infrastructure.database.mysql_config import engine, async_sessionmaker_instance
from fastapi.middleware.cors import CORSMiddleware
from backend.interfaces.api.v1.admin.document_type_routes import router as document_type_router
from backend.interfaces.api.v1.user.document_type_user_routes import router as user_document_type_router
from backend.interfaces.api.v1.admin.document_field_routes import router as admin_document_field_router
from backend.interfaces.api.v1.admin.user_routes import router as user_router
from backend.interfaces.api.v1.auth.auth_routes import router as auth_router
from backend.interfaces.api.v1.user.document_download_routes import router as document_download_router
import os
from dotenv import load_dotenv
import logging


load_dotenv()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")

    async with engine.begin() as conn:
        await conn.run_sync(DocumentTypeModel.metadata.create_all)

    async with async_sessionmaker_instance() as session:
        user_repo = get_mysql_user_repository(session=session)

        existing_admin_user = await user_repo.find_by_username("admin")

        if not existing_admin_user:
            print("No admin user found. Creating initial admin user directly via repository...")

            initial_admin_password = os.getenv("INITIAL_ADMIN_PASSWORD")
            if not initial_admin_password:
                logger.error("INITIAL_ADMIN_PASSWORD not set in environment.")
                raise ValueError("INITIAL_ADMIN_PASSWORD environment variable is required for initial admin creation.")

            import bcrypt
            password_hash_bytes = bcrypt.hashpw(initial_admin_password.encode('utf-8'), bcrypt.gensalt())
            password_hash_str = password_hash_bytes.decode('utf-8')

            from backend.core.value_objects.hashed_password import HashedPassword
            hashed_password_vo = HashedPassword(value=password_hash_str)

            from backend.core.enums.user_role_enum import UserRole

            initial_admin_entity = User(
                id=None,
                username="admin",
                email="admin@docugeniusai.local",
                hashed_password=hashed_password_vo,
                role=UserRole.ADMIN,
                is_active=True,
                created_by_user_id=None
            )

            saved_admin_entity = await user_repo.save(initial_admin_entity)

            print(
                f"Initial admin user created successfully. Username: {saved_admin_entity.username}, ID: {saved_admin_entity.id}")
            print("*** IMPORTANT: Change this password immediately after your first login! ***")
        else:
            print(f"Admin user 'admin' already exists (ID: {existing_admin_user.id}). Skipping initial admin creation.")






    print("Application started successfully!")
    yield
    print("Shutting down application...")


security_scheme = HTTPBearer(
    scheme_name="JWT",
    description="JWT authorization header using the Bearer scheme. Example: 'Bearer YOUR_JWT_ACCESS_TOKEN'",
    auto_error=True
)

app = FastAPI(title="DocuGeniusAI API", lifespan=lifespan, openapi_security=[{"JWT": []}])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(document_type_router, prefix="/api/v1/admin")
app.include_router(user_document_type_router, prefix="/api/v1/user")
app.include_router(document_download_router, prefix="/api/v1/user")
app.include_router(admin_document_field_router, prefix="/api/v1/admin")
app.include_router(user_router, prefix="/api/v1/admin")


@app.get("/")
async def root():
    return {"message": "DocuGeniusAI API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}