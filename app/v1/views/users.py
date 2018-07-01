from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint
from app.v1.views.utils import sign_up, verify_registration_data, log_in

from env_config import API_KEY

SECRET_KEY = API_KEY


users = Blueprint('users', __name__, url_prefix='/api/v1')


@users.route('/auth/signup', methods=['POST'])
@swag_from('api_doc/user_registration.yml')
def register_user():
    """
    This function enables new users to signup. ensures that the usernames and email fields are unique in the database
    :return: returns a confirmation message
    """

    data = request.get_json()
    try:
        if data['category'] and data['email'] and data['username'] and data['first_name'] and data['last_name'] \
                and data['password'] and data['confirm_password'] and data['address']:
            pass
    except KeyError:
        return make_response(jsonify(dict(message='PROVIDE ALL REQUIRED INFORMATION.')), 400)

    error_response = verify_registration_data(category=data['category'], email=data['email'], username=data['username'],
                                        first_name=data['first_name'], last_name=data['last_name'],
                                        password=data['password'], confirm_password=data['confirm_password'],
                                        address=data['address'])

    if error_response:
        return make_response(jsonify({'message': error_response['message']}), error_response['status_code'])

    new_sign_up = sign_up(category=data['category'], email=data['email'], username=data['username'],
                          first_name=data['first_name'], last_name=data['last_name'], password=data['password'],
                          confirm_password=data['confirm_password'], address=data['address'])

    return make_response(jsonify({'message': new_sign_up['message']}), new_sign_up['status_code'])


@users.route('/auth/login', methods=['POST'])
@swag_from('api_doc/user_login.yml')
def login():
    """
    This function logs in users
    :return: returns a token valid for 30 minutes
    """
    data = request.get_json()
    try:
        if data['category'] and data['username'] and data['password']:
            pass
    except KeyError:
        return make_response(jsonify({'message': 'Invalid Username or Password'}), 401)

    new_login = log_in(category=data['category'], username=data['username'], password=data['password'])

    if new_login['operation']:
        return make_response(jsonify({'token': new_login['token']}), new_login['status_code'])
    return make_response(jsonify({'message': new_login['message']}), new_login['status_code'])

