from flask import Blueprint

geographic_centre = Blueprint(
    'geographic_centre', 
    __name__, 
    template_folder='templates', 
    static_folder='static',
    url_prefix='/geographic-centre')

from . import routes 