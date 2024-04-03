from sqlalchemy import Enum

class Role(Enum):
    ADMIN = "admin"
    STAFF = "staff"