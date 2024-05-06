from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.commons import Base
from app.controllers.baseController import BaseController
from app.controllers.mitarbeiterController import MitarbeiterController
from app.controllers.zugController import ZugController
from app.models.mitarbeiter import Mitarbeiter
from app.models.zug import Zug


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
        self.baseController = BaseController(self.Session)
        self.insert_testdata()

    def init_engine(self, path):
        print(f"Database path: {path.resolve()}")
        engine = create_engine(f'sqlite:///{path.resolve()}')
        return engine

    if __name__ == "__main__":
        db_path = Path('.') / 'data' / 'database.db'
        __init__(db_path)

    def insert_testdata(self):
        self.Session.query(Mitarbeiter).delete()
        self.Session.query(Zug).delete()

        newZug = Zug(name="ICE 123", spurenweite=1435)
        addedZug = self.baseController.add(newZug)
        print("Added Zug: " + str(addedZug))

        newMitarbeiter = Mitarbeiter(name="Hansi Hanspeter", svnr="12345678", username="1", role="admin")
        newMitarbeiter.set_password("12")
        addedMitarbeiter = self.baseController.add(newMitarbeiter)
        print("Added Mitarbeiter: " + str(addedMitarbeiter))


    def get_controller(self, name):
        if name == 'base':
            return BaseController(self.Session)
        elif name == 'zug':
            return ZugController(self.Session)
        elif name == 'ma':
            return MitarbeiterController(self.Session)
        else:
            raise ValueError(f"No controller found for name: {name}")


