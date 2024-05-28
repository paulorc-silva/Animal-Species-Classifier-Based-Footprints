from flask import Blueprint
import controller.animal_controller as controller

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(controller.index)
blueprint.route('/', methods=['POST'])(controller.predict)