from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import expression

from data.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

Base = declarative_base()
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
session_class = sessionmaker(bind=engine)


class UtcNow(expression.FunctionElement):
    type = DateTime()


@compiles(UtcNow, 'postgresql')
def pg_utc_now():
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


def commit_session(session):
    try:
        session.commit()
        return True
    except DatabaseError as e:
        session.rollback()
        print(e.orig.pgerror)
        return False


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        if not commit_session(session):
            return False, False
        return instance, True


class Profile(Base):
    __tablename__ = 'client_profile'
    id = Column(Integer, primary_key=True)
    # TODO Need to refactoring to string
    external_id = Column(Integer)

    name = Column(String(60))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<Profile(name="{self.name}", external_id="{self.external_id}")>'


class Account(Base):
    __tablename__ = 'client_account'
    id = Column(Integer, primary_key=True)
    profile_id = Column(ForeignKey('client_profile.id'), nullable=False, index=True)
    account = Column(String(8), nullable=True)
    address = Column(String(120), nullable=True)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    profile = relationship('Profile')

    def __repr__(self):
        return f'<Account(profile="{self.profile}", account="{self.account}")>'
