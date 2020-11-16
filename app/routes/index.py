from flask import Blueprint

overview = Blueprint('index', __name__)

@overview.route('/')
def index():
    return 'There is no ignorance, there is knowledge.'
