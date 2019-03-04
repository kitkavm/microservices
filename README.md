# microservices

To initialize the database doing the following:

export FLASK_APP=microservices

flask init_db

# user create
curl -v -d '{"username": "kevin", "password": "12345"}' -H "Content-Type: application/json" -X POST localhost:5000/users

# change password
curl -v -u kevin:12345 -d '{"password":"12345"}' -H "Content-Type: application/json" -X PUT localhost:5000/users/kevin

# Delete User
curl -v -u kevin:12345 -H "Content-Type: application/json" -X DELETE localhost:5000/users/kevin

