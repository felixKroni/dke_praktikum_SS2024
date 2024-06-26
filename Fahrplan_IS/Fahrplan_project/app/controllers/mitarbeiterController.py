from app.controllers.baseController import BaseController
from app.models.mitarbeiter import Mitarbeiter


class MitarbeiterController(BaseController):
    def __init__(self, session):
        super().__init__(session)

    def get_mitarbeiter_by_username(self, username):
        return self.session.query(Mitarbeiter).filter(Mitarbeiter.username == username).first()

    def get_mitarbeiter_by_email(self, email):
        return self.session.query(Mitarbeiter).filter(Mitarbeiter.email == email).first()

    def get_mitarbeiter_by_role(self, role):
        return self.session.query(Mitarbeiter).filter(Mitarbeiter.role == role).all()

    def does_admin_exist(self):
        return self.session.query(Mitarbeiter).filter(Mitarbeiter.role == "admin").first() is not None




