from sqlalchemy import create_engine

from app.config import Config


def get_db_engine():
    config = Config()

    URL = (
        f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}"
        f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )

    return create_engine(URL, echo=True)


engine = get_db_engine()
