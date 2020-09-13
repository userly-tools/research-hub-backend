# Userly Tools Backend

The REST API for Userly research hub.

## Setup

### 1.Initialize the db

```bash
rohan@rohan-X556UQK ~/D/f/research-hub-backend (master)> python                                                                                                                            (fosshack) 
Python 3.8.5 (default, Sep  4 2020, 07:30:14) 
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from server import db
/home/rohan/anaconda3/envs/fosshack/lib/python3.8/site-packages/flask_sqlalchemy/__init__.py:833: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  warnings.warn(FSADeprecationWarning(
>>> db.create_all()
```
### 2. Start the server!

```bash
python server.py
```

## API Usage

### Forms

Create a form
```bash
curl "http://localhost:5000/forms" 
-X POST \
-H "Content-Type: application/json" \
-d '{
   "title":"project title",
   "desc":"project description",
   "tag":"1on1",
   "incentive":"65",
   "person_uname":"admin",
   "components":[
      {
         "id":"0",
         "is_required":"true",
         "options":"undefined",
         "question":"Hello There?",
         "type":"long_ans"
      },
      {
         "id":"0",
         "is_required":"true",
         "options":"undefined",
         "question":"Hello There?",
         "type":"long_ans"
      },
      {
         "id":"2",
         "is_required":"undefined",
         "options":"[\\"YO \\", \\"Yo 2\\"]",
         "question":"What is htis?",
         "type":"checkbox"
      }
   ]
}'
```

Similarly you can do DELETE, PATCH and GET requests

### Persons

Create a user

```bash
curl "http://localhost:5000/persons" 
-X POST \
-H "Content-Type:application/json" \
-d {"uname":"admin","name":"UserlyTeam"}'
```
Here as well you can do DELETE, PATCH and GET requests

## Credits

The following resources were really helpful in building the backend

1. https://rahmanfadhil.com/flask-rest-api/
2. https://flask-marshmallow.readthedocs.io/en/latest/
3. https://realpython.com/flask-connexion-rest-api-part-3/