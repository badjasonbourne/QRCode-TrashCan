from flask import Flask, render_template, url_for, redirect, Response
from flask_sqlalchemy import SQLAlchemy, SessionBase
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from wtforms import StringField, PasswordField, SubmitField
from flask_bcrypt import Bcrypt
import cv2 as cv
from Video import Video
from multiprocessiong import Process, Pipe
from Motor import motor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db2.db'
app.config['SECRET_KEY'] = 'thisisakey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# video = cv.VideoCapture(0)
video = Video().start()
motor = Motor()
conn1, conn2 = Pipe()
p = Process(target=motor.motion, args=(conn2))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Inf(db.Model):
    __tablename__ = 'inf'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    quality = db.Column(db.Integer)

    def __init__(self, name, quality):
        self.name = name
        self.quality = quality


db.session.add(Inf(name='Household Food Waste', quality=1))
db.session.add(Inf(name='Residual Waste', quality=1))
db.session.commit()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

               
def putsome(frame):
    cv.putText(frame, f"{video.item}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255))
    conn1.send(video.item)
    return frame

def gen_frames():
    while True:
        # ret, frame = video.read()
        frame = video.frame
        frame = putsome(frame)
        ret, buffer = cv.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


from forms import *


@app.route('/video_feed')
@login_required
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/informationn')
@login_required
def inf():
    house = Inf.query.filter_by(name='Household Food Waste').first()
    residual = Inf.query.filter_by(name='Residual Waste').first()
    return render_template('inf.html', group=[house, residual])


@app.route('/stream')
def stream():
    return render_template('stream.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('stream'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run('0.0.0.0')
    p.start()
