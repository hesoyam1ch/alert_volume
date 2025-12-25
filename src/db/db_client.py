from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db import Base
from config import settings

class DBClient:
    def __init__(self, db_url= settings.DATABASE_URL):
        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()
