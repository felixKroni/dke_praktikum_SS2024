from app.controllers.baseController import BaseController
from app.models.abschnitt import Abschnitt
from app.models.halteplan import Halteplan


class HalteplanController(BaseController):
    def __init__(self, session):
        super().__init__(session)

    def delete_abschnitt_relations(self, id):
        halteplan = self.session.query(Halteplan).get(id)
        if halteplan is not None:
            for abschnitt_halteplan in halteplan.abschnitte:
                abschnitt = self.session.query(Abschnitt).get(abschnitt_halteplan.abschnitt_id)
                self.session.delete(abschnitt)
                self.session.delete(abschnitt_halteplan)
            self.session.commit()
            return True
        else:
            return False


    def delete_abschnitt_relations_with_halteplan(self, id):
        halteplan = self.session.query(Halteplan).get(id)
        if halteplan is not None:
            for abschnitt_halteplan in halteplan.abschnitte:
                abschnitt = self.session.query(Abschnitt).get(abschnitt_halteplan.abschnitt_id)
                self.session.delete(abschnitt)
                self.session.delete(abschnitt_halteplan)

            self.session.commit()
            self.session.delete(halteplan)
            self.session.commit()
            return True
        else:
            return False


    def get_abschnitte(self, id):
        halteplan = self.session.query(Halteplan).get(id)
        if halteplan is not None:
            abschnitt_halteplan_list = halteplan.abschnitte
            abschnitt_halteplan_list = sorted(abschnitt_halteplan_list, key=lambda abschnitt_halteplan: abschnitt_halteplan.reihung)
            return [abschnitt_halteplan.abschnitt for abschnitt_halteplan in abschnitt_halteplan_list]
        else:
            return None