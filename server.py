#Reference https://rahmanfadhil.com/flask-rest-api/

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/userly.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# Delete database file if it exists currently
# if os.path.exists("data/userly.db"):
#     os.remove("data/userly.db")

# reorder! formobj then form then person

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    desc = db.Column(db.String(1024))
    num_participants = db.Column(db.Integer)
    tag = db.Column(db.String(20))
    incentive = db.Column(db.String(560))
    progress = db.Column(db.Integer)

    # researcher_uname = db.Column(db.String(16),db.ForeignKey("person.id"))
    person_uname = db.Column(db.String(16), db.ForeignKey('person.uname'))
    person = db.relationship('Person',backref='forms')

    components = db.Column(db.String(4096))
    responses = db.Column(db.String(4096))

    def __repr__(self):
        return '<Form %s>' % self.title

class FormSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Form
        include_fk = True
        fields = ('id', 'title', 'desc', 'person_uname', 'components', 'responses',
        'num_participants', 'tag', 'incentive', 'progress')


form_schema = FormSchema()
forms_schema = FormSchema(many=True)

class FormListResource(Resource):
    def get(self):
        forms = Form.query.all()
        # print(forms)
        return forms_schema.dump(forms)

    def post(self):
        new_form = Form()

        fields = FormSchema.Meta.fields

        for key in fields:
            if key in request.json:
                setattr(new_form, key, request.json[key])
        
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

class FormObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qtype = db.Column(db.String(50))
    question = db.Column(db.String(1024))

    options = db.Column(db.String(1024))
    is_required = db.Column(db.Boolean)

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
    uname = db.Column(db.String(16), unique=True, primary_key=True)
    name = db.Column(db.String(32))

    linked_users = db.Column(db.String(4096))
    # linked_forms = db.Column(db.String(4096))

    def __repr__(self):
        print(self.forms)
        return '<Person %s>' % self.uname

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        # fields = ('id', 'uname', 'name', 'linked_users', 'forms')
    uname = ma.auto_field()
    name = ma.auto_field()
    forms = ma.auto_field()
    # forms = fields.Nested('PersonFormSchema', default=[], many=True)

# class PersonFormSchema(ma.SQLAlchemyAutoSchema):
#     """
#     This class exists to get around a recursion issue
#     """
#     form_id = fields.Int()
#     person_uname = fields.Str()

person_schema = PersonSchema()
# print(person_schema)
persons_schema = PersonSchema(many=True)

fields = ('id', 'uname', 'name', 'linked_users', 'forms')

class PersonListResource(Resource):
    def get(self):
        persons = Person.query.all()
        return persons_schema.dump(persons)

    def post(self):
        new_person = Person()

        # fields = PersonSchema.Meta.fields

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

        # fields = PersonSchema.Meta.fields

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

# class Project(db.Model):
#     uname = db.Column(db.String(16), unique=True, primary_key=True)
#     name = db.Column(db.String(32))

#     linked_users = db.Column(db.String(4096))
#     # linked_forms = db.Column(db.String(4096))

#     def __repr__(self):
#         print(self.forms)
#         return '<Project %s>' % self.uname

# class ProjectSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Project
#         # fields = ('id', 'uname', 'name', 'linked_users', 'forms')
#     # uname = ma.auto_field()
#     # name = ma.auto_field()
#     # forms = ma.auto_field()

class ProjectResource(Resource):
    def get(self, person_uname):
        person = Person.query.get_or_404(person_uname)
        # print(type(person.forms))
        projlist = []
        for form_id in person.forms:
            projlist.append(Form.query.get_or_404(form_id.id))
        print(projlist)
        return forms_schema.dump(projlist)

api.add_resource(ProjectResource, '/projects/<string:person_uname>')
# @app.route('/projects')
# def get_projects():
#     persons = Person.query.all()


if __name__ == '__main__':
    # Create the database
    # db.create_all()
    app.run(debug=True)
