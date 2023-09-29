from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,decode_token
)
from flask_cors import cross_origin
from flask import  jsonify,request


from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema,JwtSchema


blp = Blueprint("Users", "users", description="Operations on users")



@blp.route("/register")

class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first():  # can be skipped and catched later via an integrity error
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "user created successfully"}, 201


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @blp.arguments(JwtSchema)
    def post(self, refresh_token):
        data=decode_token(refresh_token["refresh_token"],allow_expired=True)     
        new_token=create_access_token(identity=data["sub"], fresh=True)
        print({"access_token": new_token})
        return {"access_token": new_token}
        


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        print("login en cours 1")
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        print("login en cours 2")
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
           
            return {"access_token": access_token, "refresh_token": refresh_token,"username":user.username}, 200
        print("login non réussit")
        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    def post(self):
        # jti is the jwt unique identifier
        jti = get_jwt()[
            "jti"
        ]  # we can do .get("jti") but the jti will always be on the jwt so no need
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}
    
@blp.route("/user/<int:user_id>")

class User(MethodView):
    @blp.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
    
@blp.route("/user")
class User(MethodView):
    @jwt_required()
    def get(self):
        users = []
        user = UserModel.query.all()
        for u in user:
            users.append({"name":u.username})
        return jsonify(users)
    
    

        