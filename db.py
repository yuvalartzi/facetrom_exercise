from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///mydb', echo=True)
base = declarative_base()


# mydb = SQLAlchemy()

class FacialVectors(base):
    __tablename__ = 'facial_vectors'

    f_id = Column(Integer, primary_key=True)
    cell = Column(Integer, primary_key=True)
    x = Column(Float(precision=2))
    y = Column(Float(precision=2))
    x_mean = Column(Float(precision=2))
    y_mean = Column(Float(precision=2))
    x_std = Column(Float(precision=2))
    y_std = Column(Float(precision=2))

    def __init__(self, f_id, cell, x, y, x_mean, y_mean, x_std, y_std):
        self.f_id = f_id
        self.cell = cell
        self.x = x
        self.y = y
        self.x_mean = x_mean
        self.y_mean = y_mean
        self.x_std = x_std
        self.y_std = y_std


base.metadata.create_all(engine)
