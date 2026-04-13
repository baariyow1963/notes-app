import sqlite3
from flask import Flask, render_template, request, redirect
def list_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute(" CREATE TABLE IF NOT EXISTS notes( id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT , message TEXT ) ")
    conn.commit() 
    conn.close()
list_db()
app = Flask(__name__) 

@app.route("/")
def home():
    conn =sqlite3.connect("notes.db") 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return render_template("index.html", notes = notes) 

@app.route("/submit", methods=["POST"] )
def submit():
    username = request.form["username"]
    message = request.form["message"]
    
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute(" INSERT INTO notes ( username, message) VALUES (?,?)", ( username, message ) )
    conn.commit()
    conn.close()
    return redirect("/")
@app.route("/delete/<int:id>")
def delete(id):
    conn =sqlite3.connect("notes.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn =sqlite3.connect("notes.db")
    cursor = conn.cursor()
    if request.method == "POST":
        new_message = request.form["message"]
        cursor.execute("UPDATE notes SET message = ? WHERE id = ?", ( new_message,id ))
        conn.commit()
        conn.close()
        return redirect("/")
    cursor.execute("SELECT * FROM notes WHERE id = ?", (id,))
    note = cursor.fetchone()
    conn.close()
    return render_template("edit.html", note=note)
@app.route("/back")
def back():
    return redirect("/")
        
if __name__ == "__main__":
    app.run(debug=True)