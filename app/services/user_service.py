from app.models.user import User, db

class UserService:
    @staticmethod
    def register_user(username, email, password):
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user