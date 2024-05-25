from app.controllers.baseController import BaseController
from app.models.mitarbeiter import Mitarbeiter
from app.models.mitarbeiter_durchfuehrung import MitarbeiterDurchfuehrung


class MitarbeiterDurchfuehrungController(BaseController):
    def __init__(self, session):
        super().__init__(session)

    def remove_mitarbeiter_from_fahrtdurchfuehrung(self, fahrtdurchfuehrung_id, mitarbeiter_id):
        self.session.query(MitarbeiterDurchfuehrung).filter(MitarbeiterDurchfuehrung.fahrtdurchfuehrung_id == fahrtdurchfuehrung_id,
                                                             MitarbeiterDurchfuehrung.mitarbeiter_id == mitarbeiter_id).delete()
        self.session.commit()
