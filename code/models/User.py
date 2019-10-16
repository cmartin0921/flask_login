from db import db

class UserModel(db.Model):
  
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), nullable=False, unique=True)
  email = db.Column(db.String(), nullable=False, unique=True)
  password = db.Column(db.String(100), nullable=False)
  
  def __repr__(self):
    return f'<User: [{self.username}]>'
  
  def save(self):
    db.session.add(self)
    db.session.commit()