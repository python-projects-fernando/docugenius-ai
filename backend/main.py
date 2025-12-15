from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.infrastructure.models.document_type_model import DocumentTypeModel
from backend.infrastructure.database.mysql_config import engine, async_sessionmaker_instance
from fastapi.middleware.cors import CORSMiddleware
from backend.interfaces.api.v1.admin.document_type_routes import router as document_type_router
from backend.interfaces.api.v1.user.document_type_user_routes import router as user_document_type_router
from backend.interfaces.api.v1.admin.document_field_routes import router as admin_document_field_router
from backend.interfaces.api.v1.admin.user_routes import router as user_router
from sqlalchemy import text


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")

    async with engine.begin() as conn:
        await conn.run_sync(DocumentTypeModel.metadata.create_all)

    async with async_sessionmaker_instance() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM document_types"))
        count = result.scalar()

        if count == 0:
            print("Table 'document_types' is empty. Inserting initial records...")
            session.add(
                DocumentTypeModel(name="Service Contract", description="Standard template for service contracts."))
            session.add(DocumentTypeModel(name="Commercial Proposal",
                                          description="Template for commercial proposals sent to clients."))
            await session.commit()
            print("Initial records inserted.")
        else:
            print(f"Table 'document_types' already has {count} record(s). No initial records will be inserted.")

    print("Application started successfully!")
    yield
    print("Shutting down application...")


app = FastAPI(title="DocuGeniusAI API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_type_router, prefix="/api/v1/admin")
app.include_router(user_document_type_router, prefix="/api/v1/user")
app.include_router(admin_document_field_router, prefix="/api/v1/admin")
app.include_router(user_router, prefix="/api/v1/admin")


@app.get("/")
async def root():
    return {"message": "DocuGeniusAI API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}