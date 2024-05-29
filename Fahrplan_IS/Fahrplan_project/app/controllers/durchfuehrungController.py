from app.controllers.baseController import BaseController
from app.models import mitarbeiter
from app.models.fahrdurchfuehrung import Fahrtdurchfuehrung
from app.models.mitarbeiter import Mitarbeiter
from app.models.mitarbeiter_durchfuehrung import MitarbeiterDurchfuehrung


class DurchfuehrungController(BaseController):
    def __init__(self, session):
        super().__init__(session)

    def remove_all_mitarbeiterdurchfuehrungen_of_fahrtdurchfuehrung(self, fahrtdurchfuehrung_id):
        self.session.query(MitarbeiterDurchfuehrung).filter(MitarbeiterDurchfuehrung.fahrtdurchfuehrung_id == fahrtdurchfuehrung_id).delete()
        self.session.commit()


    def get_all_fahrtdurchfuehrungen_by_mitarbeiter_id(self, mitarbeiter_id):
        return self.session.query(Fahrtdurchfuehrung).join(MitarbeiterDurchfuehrung).filter(
            MitarbeiterDurchfuehrung.mitarbeiter_id == mitarbeiter_id).all()