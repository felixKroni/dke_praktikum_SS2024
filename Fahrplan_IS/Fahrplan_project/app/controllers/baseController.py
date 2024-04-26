from sqlalchemy.orm import Session


class BaseController:
    def __init__(self, session: Session):
        self.session = session

    def add(self, instance):
        self.session.add(instance)
        self.session.commit()
        return instance

    def delete(self, instance):
        self.session.delete(instance)
        self.session.commit()

    def update(self):
        self.session.commit()

    def find_by_id(self, model, id):
        return self.session.query(model).filter(model.id == id).first()

    def find_all(self, model):
        return self.session.query(model).all()