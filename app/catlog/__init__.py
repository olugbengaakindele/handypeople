# app/catelog/init

from flask import Blueprint

cat = Blueprint("cat", __name__, template_folder ='templates')

from app.catlog import routes 