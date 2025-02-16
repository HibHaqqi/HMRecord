from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db) 

    # Load configuration
    app.config.from_object('app.config.Config')

    from app.controller.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from app.controller.equipment_controller import eqp_bp
    app.register_blueprint(eqp_bp)

    with app.app_context():
        db.create_all()
    return app