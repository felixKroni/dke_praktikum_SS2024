from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app import Zug
from app.commons import Base
from app.controllers.baseController import BaseController


class Database:

    def __init__(self, path):
        self.engine = self.init_engine(path)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        from app.models.zug import Zug
        from app.models.fahrplan import Fahrplan
        from app.models.fahrdurchfuehrung import Fahrtdurchfuehrung
        from app.models.halteplan import Halteplan
        from app.models.abschnitt_halteplan import AbschnittHalteplan
        from app.models.abschnitt import Abschnitt
        from app.models.mitarbeiter import Mitarbeiter
        from app.models.mitarbeiter_durchfuehrung import MitarbeiterDurchfuehrung
        Base.metadata.create_all(bind=self.engine)

    def init_engine(self, path):
        print(f"Database path: {path.resolve()}")
        engine = create_engine(f'sqlite:///{path.resolve()}')
        return engine

    if __name__ == "__main__":
        db_path = Path('.') / 'data' / 'database.db'
        __init__(db_path)

    def insert_testdata(self):
        baseController = BaseController(self.Session)
        newZug = Zug(name="ICE 123", spurenweite=1435)
        addedZug = baseController.add(newZug)
        print("Added Zug: " + str(addedZug))
