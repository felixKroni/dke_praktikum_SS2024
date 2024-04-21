from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.commons import Base


def init_engine(path):
    print(f"Database path: {path.resolve()}")
    engine = create_engine(f'sqlite:///{path.resolve()}')
    return engine


def init_db(path):
    engine = init_engine(path)
    Session = scoped_session(sessionmaker(bind=engine))
    from app.models.zug import Zug
    from app.models.fahrplan import Fahrplan
    from app.models.fahrdurchfuehrung import Fahrtdurchfuehrung
    from app.models.halteplan import Halteplan
    from app.models.abschnitt_halteplan import AbschnittHalteplan
    from app.models.abschnitt import Abschnitt
    from app.models.mitarbeiter import Mitarbeiter
    from app.models.mitarbeiter_durchfuehrung import MitarbeiterDurchfuehrung
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    db_path = Path('.') / 'data' / 'database.db'
    init_db(db_path)
