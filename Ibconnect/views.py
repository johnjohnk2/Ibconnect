
from flask import  render_template,url_for, request, redirect, flash
from Ibconnect import app,db
from datetime import datetime
from Ibconnect.forms import BookmarkForm
from Ibconnect.models import User,Bookmark

def logged_in_user():
    return User.query.filter_by(username='Jonathan').first()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',new_bookmarks=Bookmark.newest(5))

@app.route('/add', methods= ['GET', 'POST'])
def add():
    form = BookmarkForm() #creation de l'instance de classe 
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm= Bookmark(user = logged_in_user(),url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Valeur enregistrée '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
    