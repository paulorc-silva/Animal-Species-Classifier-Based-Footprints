import json

from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from data.config import Base


class Animal(Base):
    __tablename__ = 'animal'

    animal_id = Column(Integer, primary_key=True)
    scientific_name = Column(String)
    common_name = Column(String)
    details = Column(String)
    photo = Column(String)

    def to_json(self):
        animal_data = self.__dict__
        animal_data.pop('_sa_instance_state', None) 
        return animal_data