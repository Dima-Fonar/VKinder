from sqlalchemy.orm import sessionmaker
from models import *


class ORM:
    def __init__(self):
        self.DSN = 'postgresql://postgres:postgres@localhost:5432/vkinder_db'
        self.engine = sq.create_engine(self.DSN)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_tables(self):
        create_tables(self.engine)

    def drop_all_tables(self):
        drop_all_tables(self.engine)

    def add_user(self, user_id, user_looking):
        date = Users(vk_id=user_id, vk_id_user_looking=user_looking)
        self.session.add(date)
        self.session.commit()

if __name__ == "__main__":
    db = ORM()
