from app.models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    @staticmethod
    def user_exists(username, email):
        return db.session.query(User).filter((User.username == username) | (User.email == email)).first() is not None

    def register_user(username, email, password):
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    @staticmethod
    def authenticate_user(email, password):
        user = db.session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return user
        return None