from flask import Flask, request
from flask_restful import Resource, Api
import backend.models as models
import os
from flask_jwt_extended import JWTManager



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'varsupersecretkeydha'
    app.config["JWT_SECRET_KEY"] = "super-secret-key"  # change later
    return app
# seperate python file for creating models
app = create_app()

models.db.init_app(app)
jwt = JWTManager(app)

from backend.routes import api
api.init_app(app)
# only one predefines admin user,it is created ,if admin already exists it does not create elseit creates a new admin user 
def create_admin():
    check_admin = models.User.query.filter_by(role=1).first()
    if not check_admin:
        admin = models.User(
            email="Admin@123",
            password="hospiadmin123",
            role=1
        )
        models.db.session.add(admin)
        models.db.session.commit()
        print("Admin Created ✅")


if __name__ == '__main__':
    with app.app_context():
        models.db.create_all()
        create_admin()

    app.run(debug=True)