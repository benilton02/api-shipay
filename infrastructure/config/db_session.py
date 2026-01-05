from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

from infrastructure.config.settings import settings


class DatabaseSession:
    """Gerenciador de sessões do banco de dados (Context Manager)"""

    _engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        echo=False,
    )

    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        try:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        except Exception:
            pass

    _SessionLocal = sessionmaker(
        bind=_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    def __enter__(self) -> Session:
        """Abre a sessão do banco de dados"""
        self.session: Session = self._SessionLocal()
        return self.session

    def __exit__(self, *args, **kwargs) -> None:
        """Fecha a sessão do banco de dados"""
        self.session.close()
