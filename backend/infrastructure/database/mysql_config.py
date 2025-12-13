import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set. Please configure it in your .env file.")

engine = create_async_engine(DATABASE_URL, echo=True)
async_sessionmaker_instance = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
