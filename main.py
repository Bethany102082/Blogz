from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQK+LALCHEMY_ECHO'] =True
db = SQLAlchemy(app)

class Entry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    post = db.Column(db.String(500))

    def __init__(self, title, post):
        self.title = title
        self.post = post

@app.route("/")
def index():            
    post_entries = Entry.query.all()
    return render_template('index.html', post_entries=post_entries)

@app.route("/make_post")
def post_entry_page():
    return render_template('post_entry_page.html')

@app.route("/my_post", methods = ["POST", "GET"])
def my_post():
    if request.method == "POST":
        title = request.form['title']
        post = request.form['post']
        title_error = ""
        post_error = ""

        if title == "":
            title_error = "Please enter a title."
        if post == "":
            post_error = "Please enter a post."
        if title == "" or post == "":   
            return render_template('post_entry_page.html', title_error=title_error, post_error=post_error, title=title, post=post)
        else:
            new_entry = Entry(title, post)
            db.session.add(new_entry)
            db.session.commit()
            saved_entry = Entry.query.get(new_entry.id)
            return render_template('saved_entry.html', saved_entry=saved_entry)    
            
    else:
        id = int(request.args.get("id"))
        saved_entry = Entry.query.get(id)
        return render_template('saved_entry.html', saved_entry=saved_entry)
if __name__ == '__main__':
    app.run()





