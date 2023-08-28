from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine


class Database:
    engine: Engine

    def __init__(self):
        self.engine = create_engine(
            "sqlite:///goverland.sqlite",
            connect_args={"check_same_thread": False},
            echo=False,
        )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


db = Database()
