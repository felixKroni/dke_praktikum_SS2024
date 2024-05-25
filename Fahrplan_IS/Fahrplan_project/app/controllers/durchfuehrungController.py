from app.controllers.baseController import BaseController
from app.models.mitarbeiter import Mitarbeiter
from app.models.mitarbeiter_durchfuehrung import MitarbeiterDurchfuehrung


class DurchfuehrungController(BaseController):
    def __init__(self, session):
        super().__init__(session)

    def remove_all_mitarbeiterdurchfuehrungen_of_fahrtdurchfuehrung(self, fahrtdurchfuehrung_id):
        self.session.query(MitarbeiterDurchfuehrung).filter(MitarbeiterDurchfuehrung.fahrtdurchfuehrung_id == fahrtdurchfuehrung_id).delete()
        self.session.commit()