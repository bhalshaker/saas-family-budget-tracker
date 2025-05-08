import database
from models import Base

database.recreate_db(Base)