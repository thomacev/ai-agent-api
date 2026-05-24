from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Engine Asíncrono
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True)

# Fábrica de sesiones
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase Base para los modelos
Base = declarative_base()