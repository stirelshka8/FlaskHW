from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, mapped_column, relationship)
from sqlalchemy import (create_engine, String, Integer, ForeignKey, URL, DateTime)
from sqlalchemy.sql.expression import func
import configuration

db_url = URL.create(
    drivername='+'.join([configuration.DB_DIALECT, configuration.DB_DRIVER]),
    username=configuration.DB_USER,
    password=configuration.DB_PASSWORD,
    host=configuration.DB_HOST,
    port=configuration.DB_PORT,
    database=configuration.DB_NAME
)
engine = create_engine(db_url, echo=True)
Session = Session(engine)


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=30), unique=True)
    email: Mapped[str] = mapped_column(String(length=30))
    pwd: Mapped[str] = mapped_column(String(length=300))

    advertisements: Mapped[list['Ads']] = relationship(back_populates='user')


class Ads(Base):
    __tablename__ = 'ads'

    id = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=30))
    description: Mapped[str] = mapped_column(String(length=300))
    date = mapped_column(DateTime, server_default=func.now())
    owner = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(back_populates='ads')


if __name__ == '__main__':
    with engine.connect() as conn:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
