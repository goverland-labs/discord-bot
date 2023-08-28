from sqlalchemy import Column, String
from src.database.database import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Server(Base):
    __tablename__ = "servers"

    server_id = Column(String, primary_key=True)
    session_id = Column(String, nullable=False)

    def __repr__(self):
        return "<Server(server_id='%s', session_id)>" % (self.space_id, self.server_id)

    @staticmethod
    def by(server_id: str):
        return db.session.query(Server).filter(Server.server_id == server_id).first()

    @staticmethod
    def create_or_update(server_id: str, session_id: str):
        if not Server.by(server_id=server_id):
            s = Server(server_id=server_id, session_id=session_id)
            db.session.add(s)
            db.session.commit()
        else:
            s = Server.by(server_id=server_id)
            s.session_id = session_id
            db.session.commit()
