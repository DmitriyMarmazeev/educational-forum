import os
import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import command
from alembic.config import Config


TEST_DB_USER = "test_user"
TEST_DB_PASS = "test_password"
TEST_DB_NAME = "test_db"

@pytest.fixture(scope="session")
def postgres_container():
    container = PostgresContainer(
        image="postgres:15",
        username=TEST_DB_USER,
        password=TEST_DB_PASS,
        dbname=TEST_DB_NAME
    )
    container.start()
    yield container
    container.stop()

@pytest.fixture(scope="session")
def test_db_url(postgres_container):
    return postgres_container.get_connection_url(driver="asyncpg")

@pytest.fixture(scope="session", autouse=True)
def setup_test_env(test_db_url):
    """Гарантирует, что приложение подхватит тестовый URL до импорта."""
    # TODO: изменить на POSTGRES_URL, когда название переменной будет исправлено в config.py
    os.environ["DATABASE_URL"] = test_db_url
    yield
    os.environ.pop("DATABASE_URL", None)

@pytest.fixture(scope="session", autouse=True)
def apply_migrations(test_db_url, setup_test_env):
    sync_db_url = test_db_url.replace("+asyncpg", "")
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", sync_db_url)
    command.upgrade(alembic_cfg, "head")
    yield

@pytest.fixture(scope="function")
def async_engine(test_db_url):
    engine = create_async_engine(
        test_db_url, 
        echo=False, 
        pool_size=1, 
        max_overflow=0,
        pool_pre_ping=True
    )
    yield engine

@pytest_asyncio.fixture(scope="function")
async def db_isolation(async_engine):
    from app.main import app
    from app.database import get_db
    from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

    async with async_engine.connect() as conn:
        await conn.begin()
        
        TestSession = async_sessionmaker(
            bind=conn, 
            class_=AsyncSession, 
            expire_on_commit=False
        )

        async def override_get_db():
            async with TestSession() as session:
                yield session

        app.dependency_overrides[get_db] = override_get_db
        yield
        app.dependency_overrides.pop(get_db, None)
        
        try:
            await conn.rollback()
        except Exception:
            pass

@pytest_asyncio.fixture()
async def client(db_isolation):
    """Асинхронный HTTP-клиент, привязанный к ASGI-приложению."""
    from app.main import app
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture()
def register_data():
    data = {
        'email': 'test@example.com',
        'name': 'test_name',
        'surname': 'test_surname',
        'password': 'test112233'
    }
    yield data
