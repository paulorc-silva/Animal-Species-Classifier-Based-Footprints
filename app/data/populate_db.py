from .config import Session
from model.animal import Animal


def insert_animals_data():
    session = Session()
    data = [
        {'animal_id': 0, 'scientific_name': 'Canis latrans', 'common_name': 'Coiote', 'details': 'https://www.inaturalist.org/taxa/42051-Canis-latrans', 'photo': 'https://static.inaturalist.org/photos/10963085/medium.jpg'},
        {'animal_id': 1, 'scientific_name': 'Lynx rufus', 'common_name': 'Lince-pardo', 'details': 'https://www.inaturalist.org/taxa/41976-Lynx-rufus', 'photo': 'https://inaturalist-open-data.s3.amazonaws.com/photos/60028871/medium.jpg'},
        {'animal_id': 2, 'scientific_name': 'Odocoileus virginianus', 'common_name': 'Veado-da-Virgínia', 'details': 'https://www.inaturalist.org/taxa/42223-Odocoileus-virginianus', 'photo': 'https://inaturalist-open-data.s3.amazonaws.com/photos/110157765/medium.jpg'}
    ]


    for d in data:
        existing_animal = session.query(Animal).filter_by(animal_id=d['animal_id']).first()

        if existing_animal:
            print(existing_animal.to_json())
        else:
            animal = Animal(**d)
            session.add(animal)

    session.commit()