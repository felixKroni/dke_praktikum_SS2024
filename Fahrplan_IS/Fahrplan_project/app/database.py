from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base


def init_engine():
    db_path = Path('.') / 'data' / 'database.db'
    engine = create_engine(f'sqlite:///{db_path.resolve()}')
    return engine



def init_db():
    Base = declarative_base()
    engine = init_engine()
    Session = scoped_session(sessionmaker(bind=engine))
    from app.models.zug import Zug
    from app.models.fahrplan import Fahrplan
    from app.models.fahrdurchfuehrung import Fahrtdurchfuehrung
    from app.models.halteplan import Halteplan
    from app.models.abschnitt_halteplan import AbschnittHalteplan
    from app.models.abschnitt import Abschnitt
    from app.models.mitarbeiter_durchfuehrung import MitarbeiterDurchfuehrung

    Base.metadata.create_all(bind=engine)



if __name__ == "__main__":
    init_db()