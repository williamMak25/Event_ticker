from flask import Flask
from extensions import db
from flask_session import Session
from api.routes import api
from pages.route import pages

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.register_blueprint(api)
    app.register_blueprint(pages)
    db.init_app(app)
    Session(app)
    # import models AFTER db.init_app
    with app.app_context():
        from schemas.user import User
        from schemas.events import Event
        from schemas.secondary_tables import user_events
        from schemas.tickets import Ticket
        from schemas.payment import Wallet,Transtions
        db.create_all()
    
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)