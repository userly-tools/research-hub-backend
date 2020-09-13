# research-hub-backend

The REST API for Userly research hub.

## Usage

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
### Persons

Create a user

```bash
curl "http://localhost:5000/persons" 
-X POST \
-H "Content-Type:application/json" \
-d {"uname":"admin","name":"UserlyTeam"}'
```

## Credits

The following resources were really helpful in building the backend

1. https://rahmanfadhil.com/flask-rest-api/
2. https://flask-marshmallow.readthedocs.io/en/latest/
3. https://realpython.com/flask-connexion-rest-api-part-3/