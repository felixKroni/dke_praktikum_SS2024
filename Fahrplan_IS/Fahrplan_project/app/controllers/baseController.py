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

    def delete_multiple(self, instances):
        for instance in instances:
            self.session.delete(instance)
        self.session.commit()

    def delete_all(self, model):
        self.session.query(model).delete()
        self.session.commit()

    def commit(self):
        self.session.commit()

    def update(self, instance, new_data):
        for key, value in new_data.items():
            setattr(instance, key, value)

        self.session.commit()

    def update_by_id(self, model, id, new_data):
        instance = self.find_by_id(model, id)
        if instance:
            self.update(instance, new_data)
            self.session.commit()
            return new_data
        else:
            print(f"No instance found with id {id}.")

    def find_by_id(self, model, id):
        return self.session.query(model).filter(model.id == id).first()

    def find_all(self, model):
        return self.session.query(model).all()
