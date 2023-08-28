from database.models import Base
from database.database import db


def main():
    Base.metadata.create_all(db.engine)


if __name__ == "__main__":
    main()
