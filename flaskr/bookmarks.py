from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests
from bs4 import BeautifulSoup

bp = Blueprint('bookmarks', __name__)

@bp.route('/')
def index():
    db = get_db()
    bookmarks = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('bookmarks/index.html', bookmarks=bookmarks)

def get_title(url):
    try:
        # 1. Visitamos la web
        req = requests.get(url, timeout=5)
        
        # 2. Parseamos el contenido
        sopa = BeautifulSoup(req.text, 'html.parser')
        
        # 3. Extraemos el texto de la etiqueta <title>
        title = sopa.title.string if sopa.title else "Sin título"
        return title.strip()
    except:
        return "Enlace no disponible"

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        url = request.form.get('url')
        
        title = get_title(url)
        
        body = request.form.get('body')
        
        error = None

        if not url:
            error = 'La URL es obligatoria.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id']) # 'title' ahora es el nombre de la web extraído
            )
            db.commit()
            return redirect(url_for('bookmarks.index'))

    return render_template('bookmarks/create.html')

def get_post(id, check_author=True):
    bookmark = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if bookmark is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and bookmark['author_id'] != g.user['id']:
        abort(403)

    return bookmark

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    bookmark = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('bookmarks.index'))

    return render_template('bookmarks/update.html', bookmark=bookmark)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('bookmarks.index'))