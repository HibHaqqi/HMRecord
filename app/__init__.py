from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')

    # Register blueprints or routes here
    from app.controller.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    return app