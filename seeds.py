from app.models import User
from app.db import Session, Base, engine
import json

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

users_file = open('../data/users.json')
users = json.load(users_file)
users_file.close()

db = Session()

for user in users:
    user_seed = User(username = user['username'], password = user['password'], email = user['email'])
    db.add(user_seed)

db.commit()

db.close()