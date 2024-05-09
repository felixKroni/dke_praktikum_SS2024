from app.controllers.baseController import BaseController


class HalteplanController(BaseController):
    def __init__(self, session):
        super().__init__(session)