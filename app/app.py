from data.config import engine
from data.populate_db import insert_animals_data
from model import animal
from routes.blueprint import blueprint

from flask import Flask

import os


def create_app():
    app = Flask(__name__)
    app.template_folder = os.path.abspath('./app/web/templates')
    app.static_folder = os.path.abspath('./app/web/static')

    animal.Base.metadata.create_all(bind=engine)
    insert_animals_data()
    
    return app


app = create_app()
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(port=5000, debug=True)