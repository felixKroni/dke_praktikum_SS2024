from app import app
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Wagen, Triebwagen, Personenwagen, Zug, Wartung

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Wagen': Wagen,
            'Triebwagen': Triebwagen, 'Personenwagen': Personenwagen, 'Zug': Zug, 'Wartung' : Wartung}