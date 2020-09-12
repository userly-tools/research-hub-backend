#Reference https://rahmanfadhil.com/flask-rest-api/

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/userly.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    desc = db.Column(db.String(1024))

    researcher_uname = db.Column(db.String(16))

    components = db.Column(db.String(4096))
    responses = db.Column(db.String(4096))

    def __repr__(self):
        return '<Form %s>' % self.title

class FormSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'desc', 'researcher_uname', 'components', 'responses')

form_schema = FormSchema()
forms_schema = FormSchema(many=True)

class FormListResource(Resource):
    def get(self):
        forms = Form.query.all()
        return forms_schema.dump(forms)

    def post(self):
        new_form = Form()

        fields = FormSchema.Meta.fields

        for key in fields:
            if key in request.json:
                setattr(form, key, request.json[key])

        db.session.add(new_form)
        db.session.commit()
        return form_schema.dump(new_form)

api.add_resource(FormListResource, '/forms')

class FormResource(Resource):
    def get(self, form_id):
        form = Form.query.get_or_404(form_id)
        return form_schema.dump(form)

    def patch(self, form_id):
        form = Form.query.get_or_404(form_id)

        fields = FormSchema.Meta.fields

        for key in fields:
            if key in request.json:
                setattr(form, key, request.json[key])

        db.session.commit()
        return form_schema.dump(form)

    def delete(self, form_id):
        form = Form.query.get_or_404(form_id)
        db.session.delete(form)
        db.session.commit()
        return '', 204

api.add_resource(FormResource, '/forms/<int:form_id>')

# ----------------------------------------------------------------

class FormObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qtype = db.Column(db.String(50))
    question = db.Column(db.String(1024))

    options = db.Column(db.String(1024))
    is_required = db.Column(db.String(1))

    def __repr__(self):
        return '<FormObject %s>' % self.qtype

class FormObjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'qtype', 'question', 'options', 'is_required')

form_object_schema = FormObjectSchema()
form_objects_schema = FormObjectSchema(many=True)

class FormObjectListResource(Resource):
    def get(self):
        forms = FormObject.query.all()
        return form_objects_schema.dump(forms)

    def post(self):
        new_form_object = FormObject()

        fields = FormObjectSchema.Meta.fields

        for key in fields:
            if key in request.json:
                setattr(new_form_object, key, request.json[key])

        db.session.add(new_form_object)
        db.session.commit()
        return form_object_schema.dump(new_form_object)

api.add_resource(FormObjectListResource, '/form_objects')

class FormObjectResource(Resource):
    def get(self, form_object_id):
        form_object = FormObject.query.get_or_404(form_object_id)
        return form_object_schema.dump(form_object)

    def patch(self, form_object_id):
        form_object = FormObject.query.get_or_404(form_object_id)

        fields = FormObjectSchema.Meta.fields

        for key in fields:
            if key in request.json:
                setattr(form_object, key, request.json[key])

        db.session.commit()
        return form_object_schema.dump(form_object)

    def delete(self, form_object_id):
        form_object = FormObject.query.get_or_404(form_object_id)
        db.session.delete(form_object)
        db.session.commit()
        return '', 204

api.add_resource(FormObjectResource, '/form_objects/<int:form_object_id>')

# ----------------------------------------------------------------

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(16))
    name = db.Column(db.String(32))

    linked_users = db.Column(db.String(4096))
    linked_forms = db.Column(db.String(4096))

    def __repr__(self):
        return '<Person %s>' % self.uname

class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'uname', 'name', 'linked_users', 'linked_forms')

person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)

class PersonListResource(Resource):
    def get(self):
        persons = Person.query.all()
        return persons_schema.dump(persons)

    def post(self):
        new_person = Person()

        fields = PersonSchema.Meta.fields

        for key in fields:
            if key in request.json:
                setattr(new_person, key, request.json[key])
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person)

api.add_resource(PersonListResource, '/persons')

class PersonResource(Resource):
    def get(self, person_id):
        person = Person.query.get_or_404(person_id)
        return person_schema.dump(person)

    def patch(self, person_id):
        person = Person.query.get_or_404(person_id)

        fields = PersonSchema.Meta.fields

        for key in fields:
            if key in request.json:
                setattr(person, key, request.json[key])

        db.session.commit()
        return person_schema.dump(person)

    def delete(self, person_id):
        person = Person.query.get_or_404(person_id)
        db.session.delete(person)
        db.session.commit()
        return '', 204

api.add_resource(PersonResource, '/persons/<int:person_id>')

if __name__ == '__main__':
    app.run(debug=True)
