# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack

# configuration
DATABASE = 'scroll.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = '1'
PASSWORD = '1'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


"""def init_db():
    #Creates the database tables.
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
"""

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db


@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select id, surname, name, patronymic, company, post, number, status from intruders order by id asc')
    intruders = cur.fetchall()
    return render_template('show_entries.html', intruders=intruders)

@app.route('/login_entries')
def show_entries():
    db = get_db()
    cur = db.execute('select id, surname, name, patronymic, company, post, number, status from intruders order by id asc')
    intruders = cur.fetchall()
    return render_template('login_entries.html', intruders=intruders)

"""@app.route('/show_detail/<id>')
def show_detail(id):
    db = get_db()
    cur = db.execute('select * from entries where id = ?', [id])
    entries = cur.fetchall()
    return render_template('show_detail.html', entries=entries)
	
@app.route('/edit/<id>')
def show_detail(id):
    db = get_db()
    cur = db.execute('select * from entries where id = ?', [id])
    entries = cur.fetchall()
    return render_template('show_detail.html', entries=entries)
	
@app.route('/detail', methods=['GET'])
def detail():
    db = get_db()
    db.execute('select f, i, o, c, t, s, n1d, n1t, n1w, n1r, n1p from entries order by asc'
	entries = cur.fetchall()
    return redirect(url_for('show_entries'))"""
	
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into intruders (surname, name, patronymic, company, post, number, status) values (?, ?, ?, ?, ?, ?, ?)',
                 [request.form['surname'], request.form['name'], request.form['patronymic'], request.form['company'], request.form['post'], request.form['number'], request.form['status']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('login_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
#    init_db()
    app.run(debug=True)
