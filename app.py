from flask import Flask, render_template
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nanbargal.db'
#initilaize the db
db = SQLAlchemy(app)


#create db model
class Nanbargal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # create a function to return a string when we add more
    def __repr__(self):
        return '<Name %r>' % self.id
    


subscribers = []


@app.route('/prandss', methods=['POST', 'GET'])
def prandss():
    title = "Friends.."
    friend_name = None  # Initialize the friend_name variable
     

    if request.method == "POST":
        friend_name = request.form['name'] 
         # Set friend_name to the entered name
        print(f"Friend Name: {friend_name}")
        new_friend = Nanbargal(name=friend_name)

        # push to db
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/prandss')
        except:
            return "There was an error adding your friend"

    friends = Nanbargal.query.order_by(Nanbargal.date_created)
    return render_template("prandss.html", title=title, friends=prandss, friend_name=friend_name)

@app.route('/')
def index():
    title = "Anush's Portfolio"
    return render_template("index.html", title=title)

@app.route('/about')
def about():
    title = "About Anush!"
    names = ["Anush", "Pixie", "Pebbles"]
    return render_template("about.html", names=names, title=title)


@app.route('/subscribe')
def subscribe():
    title = "Subscribe my channel"
    return render_template("subscribe.html", title=title)

@app.route('/form', methods=["POST"])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email") 

   #message = "You have been subscribed to my email"
   # server = smtplib.SMTP("smtp.gmail.com", 587)
   # server.starttls()
   # server.login("abanush1718@gmail.com", "" )
   # server.sendmail("abanush1718@gmail.com", email, message)


    if not first_name or not last_name or not email:
        error_statement = "Ella Dabbas should be filled"
        return render_template("subscribe.html", error_statement=error_statement, first_name=first_name, last_name=last_name, email=email)

    subscribers.append(f"{first_name} {last_name} | {email}")
    title = "Nandri"
    return render_template("form.html", title=title, subscribers=subscribers)


if __name__ == '__main__':
    with app.app_context():
       db.create_all()
    app.run(debug=True)