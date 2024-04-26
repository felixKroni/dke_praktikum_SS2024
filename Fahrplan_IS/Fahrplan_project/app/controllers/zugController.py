from app.controllers.baseController import BaseController
from app.models.zug import Zug


class ZugController(BaseController):
    def __init__(self, session):
        super().__init__(session)

    def get_zug_by_name(self, name):
        return self.session.query(Zug).filter(Zug.name == name).first()
