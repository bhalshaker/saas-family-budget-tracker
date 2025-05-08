import database
from models import Base
import asyncio

asyncio.run(database.recreate_db(Base))