from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:blogz@localhost:8889/Blogz'
app.config['SQK+LALCHEMY_ECHO'] =True
db = SQLAlchemy(app)
app.secret_key = 'winnieandlouie'

class User(db.Model):

    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    entries = db.relationship('Entry', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        

class Entry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    post = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, post, owner):
        self.title = title
        self.post = post
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes = ['user_signup', 'user_login']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

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
            owner = User.query.filter_by(username=session['username']).first()
            new_entry = Entry(title, post, owner)
            db.session.add(new_entry)
            db.session.commit()
            saved_entry = Entry.query.get(new_entry.id)
            return render_template('saved_entry.html', saved_entry=saved_entry)    
            
    else:
        id = int(request.args.get("id"))
        saved_entry = Entry.query.get(id)
        return render_template('saved_entry.html', saved_entry=saved_entry)

@app.route("/login", methods = ['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/make_post')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route("/signup", methods = ['POST', 'GET'])
def user_signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        verify_pw = request.form['verify_pw']
        un_error = ""
        pw_error = ""
        pwvr_error = ""

        valid = True
        if len(username) < 3 or len(username) > 20 or " " in username:
            un_error = "Must contain 3 to 20 characters"
            valid = False
        if len(password) < 3 or len(password) > 20 or " " in password:
            pw_error = "Must contain 3 to 20 characters"
            valid = False
        if password != verify_pw:
            pwvr_error = "Passwords do not match"
            valid = False
            
        if valid == False:
            return render_template('signup.html', username=username, un_error=un_error, pw_error=pw_error, pwvr_error=pwvr_error)
        else:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/make_post')
            else:
                flash('User already exists.', 'error')

            return render_template('signup.html')
    else:
        return render_template('signup.html')      

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')      

@app.route('/authors')
def authors():
    authors = User.query.all()   
    return render_template('authors.html', authors=authors) 

@app.route('/author')
def author():
    id = int(request.args.get("id"))
    user = User.query.get(id)
    post_entries = Entry.query.filter_by(owner=user).all()
    return render_template('dynamic.html', post_entries=post_entries)



if __name__ == '__main__':
    app.run()





