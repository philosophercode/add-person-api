from app import db, ma

# DB Model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    dob = db.Column(db.DateTime, unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.name

class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name','age','dob','email')

person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)