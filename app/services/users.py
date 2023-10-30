from flask_jwt_extended import get_jwt_identity
from app import db, jwt
from app.models.user import User


def create_user(name):
    """Creates a new user"""
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return user


def is_user(user_id, name):
    """Validates id and name of an user"""
    user = db.session.get(User, user_id)
    if not user:
        return False
    return user.name == name


def first_user():
    """Creates a first and default user"""
    user = User.query.first()
    if not user:
        user = create_user("First User")
    print("\033[92mFirst user token:\033[00m")
    print(f"\t{user.calculate_token()}")


@jwt.user_identity_loader
def find_user(_jwt_header, jwt_data):
    """Looks for a user in the token"""
    user_id = jwt_data["sub"]
    return db.session.get(User, id=int(user_id))


def delete_user(user_id):
    """Deletes an user"""
    user = db.session.get(User, user_id)
    if not user:
        raise FileNotFoundError
    db.session.delete(user)
    db.session.commit()


def user_to_dict(user):
    """Converts task object to dictionary"""
    return {
        'id': user.id,
        'name': user.name,
        'token': user.calculate_token()
    }

def get_users():
    """Get all users"""
    users = User.query.all()
    return [user_to_dict(x) for x in users]
