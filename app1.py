from flask import Flask, flash, redirect,render_template,request,redirect

from flask_login import LoginManager,login_user,UserMixin, logout_user

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt,bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app) 


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'secretkey'  
db = SQLAlchemy(app)
login_manager = LoginManager() 
login_manager.init_app(app)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(120), nullable=False)
    

    def __repr__(self):
        return '<User %r>' % self.name



class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120),nullable=False)
    

    def __repr__(self):
        return '<Blog %r>' % self.content



@app.route("/")
def Index():
    data = Blog.query.all()
    return render_template("register.html",data=data)



@app.route("/main")
def Home():
    return render_template("main.html")


@app.route("/index")
def index():
    data = Blog.query.all()
    return render_template("index.html",data=data)



@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        enc_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name,email=email,password=enc_password)
        db.session.add(user)
        db.session.commit()
        flash('user Registerd Successfully!','Success')  
        return redirect("/login")

    return render_template('register.html')


@login_manager.user_loader
def load_user(user_id):              
    return User.query.get(int(user_id))



@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and password == user.password:
            login_user(user)
            return redirect('/index')
        else:
            flash('Email and password did not matched!!!','warning')
            return redirect('/login')
    else:
        return render_template("login.html")



@app.route("/detail/<int:id>",methods=['GET','POST'])
def blogdetail(id):
    blog = Blog.query.get(id)
    return render_template("/detail.html",blog=blog)



@app.route("/logout")
def logout():
    logout_user()
    flash('user logout successfully!!!','success')
    return render_template('login.html')


@app.route("/blogpost",methods=['GET','POST']) 
def blogpost():
    if request.method == 'POST':
        content = request.form.get('content')
        blog = Blog(content=content)
        db.session.add(blog)
        db.session.commit()
        return redirect('/index')
    return render_template('blog.html')



if __name__ == "__main__":
    app.run(debug=True)