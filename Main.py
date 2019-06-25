from flask import Flask,render_template,redirect,url_for,logging,session,request,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt
engine=create_engine("mysql+pymysql://root:rootpw@localhost/register")
                    #("mysql+pymysql://Username:Password@localhost/dbname")
db=scoped_session(sessionmaker())
db.configure(bind=engine)
app = Flask(__name__)

@app.route("/")
def home() :
    return render_template("home.html")


#register form
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        secure_password=sha256_crypt.encrypt(str(password))

        if password == confirm:
            db.execute("insert into users(name, username, password) values(:name,:username, :password)",
                                            {"name":name,"username":username,"password":secure_password })
            db.commit()
            flash("You have successfully registered please continue to login","success")
            return redirect(url_for("login"))
        else:
            flash(u"Passwords do not match","danger")
            return render_template("register.html")

    return render_template("register.html")

#login
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username=request.form.get("name")
        password=request.form.get("password")

        usernamedata = db.execute("select username from users where username= :username",{"username":username}).fetchone()
        passworddata = db.execute("select password from users where username= :username",{"username":username}).fetchone()

        if usernamedata is None:
            flash("No username","danger")
            return render_template("login.html")
        else:
            for password_data in passworddata:
                if sha256_crypt.verify(password,password_data):
                    session["log"] = True
                    flash("You have now logged in successfully","success")
                    return redirect(url_for("photo"))
                else:
                    flash("Incorrect password","danger")
                    return render_template("login.html")
    return render_template("login.html")
#photo
@app.route("/photo")
def photo():
    return render_template("photo.html")

#logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You are now successfully logged out of your account","success")
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.secret_key="1234567JAK"
    app.run(debug=True)
