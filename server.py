#Reference https://rahmanfadhil.com/flask-rest-api/

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/userly.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# ----------------------------------------------------------------

class FormObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sort_id = db.Column(db.Integer)
    qtype = db.Column(db.String(50))
    question = db.Column(db.String(1024))

    options = db.Column(db.String(1024))
    is_required = db.Column(db.String)

    parent_form_id = db.Column(db.Integer,db.ForeignKey('form.id'))
    form = db.relationship('Form',backref='components')
    
    def __init__(self,sort_id,is_required,options,question,qtype):
        self.is_required = is_required
        self.options = options
        self.question = question
        self.qtype = qtype
        self.sort_id = sort_id
    def __repr__(self):
        return '<FormObject %s>' % self.qtype

class FormObjectSchema(ma.SQLAlchemySchema):
    class Meta:
        model = FormObject
        include_fk = True
        fields = ('id', 'qtype', 'question', 'options', 'is_required', 'parent_form_id')

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

class Person(db.Model):
    uname = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(32))

    linked_users = db.Column(db.String(4096))
    # linked_forms = db.Column(db.String(4096))

    def __repr__(self):
        print(self.forms)
        return '<Person %s>' % self.uname

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    desc = db.Column(db.String(1024))
    num_participants = db.Column(db.Integer)
    tag = db.Column(db.String(20))
    incentive = db.Column(db.String(560))
    progress = db.Column(db.Integer)

    person_uname = db.Column(db.String(16), db.ForeignKey('person.uname'))
    person = db.relationship('Person',backref='forms')

    responses = db.Column(db.String(4096))

    def __repr__(self):
        return '<Form %s>' % self.title

class FormSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Form
        include_fk = True
        fields = ('id', 'title', 'desc', 'person_uname', 'responses',
        'num_participants', 'tag', 'incentive', 'progress','components')
    components = ma.auto_field()

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
            if key in request.json and key != 'components':
                setattr(new_form, key, request.json[key])
        
        for elem in request.json['components']:
            new_form.components.append(FormObject(elem['id'],
            elem['is_required'],elem['options'],elem['question'],
            elem['type']))
        
        p = Person.query.get_or_404(new_form.person_uname)
        p.forms.append(new_form)

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



class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        fields = ('id', 'uname', 'name', 'linked_users', 'forms')
    uname = ma.auto_field()
    name = ma.auto_field()
    forms = ma.auto_field()

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
    def get(self, person_uname):
        person = Person.query.get_or_404(person_uname)
        return person_schema.dump(person)

    def patch(self, person_uname):
        person = Person.query.get_or_404(person_uname)

        fields = PersonSchema.Meta.fields

        for key in fields:
            if key in request.json:
                setattr(person, key, request.json[key])

        db.session.commit()
        return person_schema.dump(person)

    def delete(self, person_uname):
        person = Person.query.get_or_404(person_uname)
        db.session.delete(person)
        db.session.commit()
        return '', 204

api.add_resource(PersonResource, '/persons/<string:person_uname>')

class ProjectResource(Resource):
    def get(self, person_uname):
        person = Person.query.get_or_404(person_uname)
        projlist = []
        for form_id in person.forms:
            projlist.append(Form.query.get_or_404(form_id.id))
        return forms_schema.dump(projlist)

api.add_resource(ProjectResource, '/projects/<string:person_uname>')

class FormsWithComponents(Resource):
    def get(self, form_id):
        form = Form.query.get_or_404(form_id)
        complist = []
        for form_id in form.components:
            complist.append(FormObject.query.get_or_404(form_id.id))
        
        return form_objects_schema.dump(complist)

api.add_resource(FormsWithComponents, '/form_components/<int:form_id>')

if __name__ == '__main__':
    # Create the database
    # db.create_all()
    app.run(debug=True)
