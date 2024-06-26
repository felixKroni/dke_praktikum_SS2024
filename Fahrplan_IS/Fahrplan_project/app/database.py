from pathlib import Path

import requests
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.commons import Base
from app.controllers.abschnittController import AbschnittController
from app.controllers.baseController import BaseController
from app.controllers.durchfuehrungController import DurchfuehrungController
from app.controllers.halteplanController import HalteplanController
from app.controllers.mitarbeiterController import MitarbeiterController
from app.controllers.mitarbeiter_durchfuehrungController import MitarbeiterDurchfuehrungController
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
        fake = Faker()

        #Zug Daten
        self.getZuege()

        #Default Admin
        if self.get_controller("ma").does_admin_exist() is False:
            print("No admin found, creating default...")
            newMitarbeiter = Mitarbeiter(name=fake.name(), svnr="12345678", username="admin", role="admin", email=fake.email())
            newMitarbeiter.set_password("admin")
            addedMitarbeiter = self.baseController.add(newMitarbeiter)
            print("Added Default Admin")
            print("username: admin")
            print("password: admin")
            print("change password after first login!")

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
        elif name == "df":
            return DurchfuehrungController(self.Session)
        elif name == "ma_df":
            return MitarbeiterDurchfuehrungController(self.Session)
        else:
            raise ValueError(f"No controller found for name: {name}")


    def getZuege(self):
        response = requests.get("http://127.0.0.1:5002/api/züge")
        zuege_data = response.json()
        existing_zuege = self.baseController.find_all(Zug)

        for zug_data in zuege_data:
            unique_name = zug_data["zug_name"] + ' ' + zug_data["zug_nummer"]
            existing_zug = self.get_controller("zug").get_zug_by_name(unique_name)

            if not existing_zug:
                zug = Zug(
                    name=unique_name,
                    spurenweite=zug_data["spurweite"]
                )
                self.baseController.add(zug)