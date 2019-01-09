from datetime import datetime
from attendance import db, login_manager

# UserMixin has inheiritable methods we're giving to User
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# database classes (Models)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    # this is signifying the one to many relationship from User to Note
    # TODO: learn about the lazy indicator... as well as the backref
    notes = db.relationship('Note', backref='reviewer', lazy=True)

    # this needs some more explaination...
    # seems to be what shows up in the terminal window when we return an object of this type
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    grad_class = db.Column(db.Integer, nullable=False)  # we don't want to store fresh, soph, etc.

    # one to many with Student to Note
    notes = db.relationship('Note', backref='student', lazy=True)

    def __repr__(self):
        return f"Note('{self.id}', '{self.firstname}', '{self.lastname}')"


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    note_image = db.Column(db.String(20), nullable=True)
    system_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    begin_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    content = db.Column(db.String(2000), nullable=True)

    def __repr__(self):
        return f"Note('{self.begin_date}', '{self.end_date}', '{self.content}')"
