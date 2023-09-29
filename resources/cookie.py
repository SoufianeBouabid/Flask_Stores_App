from flask import Flask, request, jsonify, make_response

from flask_smorest import Blueprint, abort

blp = Blueprint("Cookies", "cookies", description="Operations on cookies")

@blp.route('/set_cookie', methods=['GET'])
def set_cookie():
    response = make_response(jsonify({'message': 'Cookie has been set'}))
    response.set_cookie('my_cookie', 'cookie_value', max_age=3600)  # Replace 'cookie_value' with your desired value and '3600' with the desired expiration time in seconds.
    return response

