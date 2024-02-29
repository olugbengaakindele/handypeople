# app/catelog/routes
from flask import render_template
from app.catlog import cat
from app import db
from app.catlog.models import Publication, Books

@cat.route("/catelog")
def catelog():
    books =Books.query.order_by(Books.title).all()

    return render_template("cat.html", books = books )