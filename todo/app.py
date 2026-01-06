from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def connect_db():
    connection = sqlite3.connect("todo.db")
    connection.row_factory = sqlite3.Row
    return connection

with connect_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)

@app.route("/", methods=["GET", "POST"])
def home():
    db = connect_db()

    if request.method == "POST":
        new_task = request.form.get("task")

        if new_task:
            db.execute(
                "INSERT INTO todos (task) VALUES (?)",
                (new_task,)
            )
            db.commit()

        return redirect(url_for("home"))

    all_tasks = db.execute("SELECT * FROM todos").fetchall()
    db.close()

    return render_template("index.html", tasks=all_tasks)

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    db = connect_db()

    if request.method == "POST":
        updated_task = request.form.get("task")

        db.execute(
            "UPDATE todos SET task=? WHERE id=?",
            (updated_task, task_id)
        )
        db.commit()
        db.close()

        return redirect(url_for("home"))

    task = db.execute(
        "SELECT * FROM todos WHERE id=?",
        (task_id,)
    ).fetchone()

    db.close()
    return render_template("edit.html", task=task)

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    db = connect_db()

    db.execute(
        "DELETE FROM todos WHERE id=?",
        (task_id,)
    )
    db.commit()
    db.close()

    return redirect(url_for("home"))
    
if __name__ == "__main__":
    app.run(debug=True)
