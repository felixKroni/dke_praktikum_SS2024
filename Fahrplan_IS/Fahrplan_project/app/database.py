from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.commons import Base
from app.controllers.abschnittController import AbschnittController
from app.controllers.baseController import BaseController
from app.controllers.halteplanController import HalteplanController
from app.controllers.mitarbeiterController import MitarbeiterController
from app.controllers.zugController import ZugController
from app.models.abschnitt import Abschnitt
from app.models.abschnitt_halteplan import AbschnittHalteplan
from app.models.halteplan import Halteplan
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
        self.Session.query(Abschnitt).delete()
        self.Session.query(Halteplan).delete()
        self.Session.query(AbschnittHalteplan).delete()

        #Zug Data
        newZug = Zug(name="ICE 123", spurenweite=1435)
        addedZug = self.baseController.add(newZug)
        print("Added Zug: " + str(addedZug))

        #Mitarbeiter Data
        newMitarbeiter = Mitarbeiter(name="Miky", svnr="12345678", username="1", role="admin", email="miky.x@g2.at")
        newMitarbeiter.set_password("12")
        addedMitarbeiter = self.baseController.add(newMitarbeiter)
        print("Added Mitarbeiter: " + str(addedMitarbeiter))

        #Abschnitt Data
        abschnitt1 = Abschnitt(spurenweite=1.435, nutzungsentgelt=100.0, StartBahnhof="Wien", EndBahnhof="Budapest")
        abschnitt2 = Abschnitt(spurenweite=1.435, nutzungsentgelt=100.0, StartBahnhof="Budapest", EndBahnhof="Sofia")
        abschnitt3 = Abschnitt(spurenweite=1.435, nutzungsentgelt=100.0, StartBahnhof="Sofia", EndBahnhof="Istanbul")
        self.baseController.add(abschnitt1)
        self.baseController.add(abschnitt2)
        self.baseController.add(abschnitt3)


        #Halteplan Data
        halteplan1 = Halteplan(name="Orient Express Long", streckenName="Orient Route")
        self.baseController.add(halteplan1)



        #AbschnittHalteplan Data to link
        wien_budapest = AbschnittHalteplan(abschnitt_id=abschnitt1.id, halteplan_id=halteplan1.id, reihung=1)
        budapest_sofia = AbschnittHalteplan(abschnitt_id=abschnitt2.id, halteplan_id=halteplan1.id, reihung=2)
        sofia_istanbul = AbschnittHalteplan(abschnitt_id=abschnitt3.id, halteplan_id=halteplan1.id, reihung=3)

        self.baseController.add(wien_budapest)
        self.baseController.add(budapest_sofia)
        self.baseController.add(sofia_istanbul)


        #Commit
        self.Session.commit()




    def get_controller(self, name):
        if name == 'base':
            return BaseController(self.Session)
        elif name == 'zug':
            return ZugController(self.Session)
        elif name == 'ma':
            return MitarbeiterController(self.Session)
        elif name == 'hp':
            return HalteplanController(self.Session)
        elif name == 'ab':
            return AbschnittController(self.Session)
        else:
            raise ValueError(f"No controller found for name: {name}")


