# app.py - Simple Blog (Flask + SQLite)
from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
from datetime import datetime
import os
import click

DATABASE = os.path.join(os.path.dirname(__file__), 'blog.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret'  # change in production


def get_db():
    """Return a sqlite3 connection (creates one per request)."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close the DB connection at the end of request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    """Create the posts table if it doesn't exist."""
    schema = """
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        created_at TEXT NOT NULL
    );
    """
    db = sqlite3.connect(DATABASE)
    try:
        db.executescript(schema)
        db.commit()
    finally:
        db.close()


@app.cli.command("initdb")
def initdb_command():
    """Click command: python -m flask initdb  (or flask initdb)"""
    init_db()
    print("Initialized the database.")


@app.route('/')
def index():
    db = get_db()
    posts = db.execute('SELECT id, title, content, created_at FROM posts ORDER BY created_at DESC').fetchall()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post is None:
        flash('Post not found', 'warning')
        return redirect(url_for('index'))
    return render_template('view.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title:
            flash('Title is required.', 'danger')
        else:
            db = get_db()
            now = datetime.utcnow().isoformat()
            db.execute('INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)',
                       (title, content, now))
            db.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/edit/<int:post_id>', methods=('GET', 'POST'))
def edit(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post is None:
        flash('Post not found', 'warning')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title:
            flash('Title is required.', 'danger')
        else:
            db.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                       (title, content, post_id))
            db.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/delete/<int:post_id>', methods=('POST',))
def delete(post_id):
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    db.commit()
    flash('Post deleted.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Initialize DB file if missing or empty
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
