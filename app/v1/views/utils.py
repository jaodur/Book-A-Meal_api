
import jwt
import datetime
from app.v1.models.models import User, Caterer

from env_config import API_KEY

SECRET_KEY = API_KEY
# SECRET_KEY ='secretKey4512yek'


def verify_password(username, user_email, db_password, input_password, category):
    if db_password == input_password:
        token_string = str(category) + ',' + str(username) + ',' + str(user_email)
        token = jwt.encode({'info': token_string,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           SECRET_KEY)
        return token.decode('UTF-8')
    return False


def verify_input_data(**input_data):
    for data in input_data.values():
        if not data:
            return False

    at_char_found, at_count, period_count = False, 0, 0

    for char in input_data['email']:
        if char == '@':
            at_count += 1
            at_char_found = True

        if at_char_found and char == '.':
            period_count += 1

    if at_count != 1:
        return False
    if period_count != 1:
        return False
    return True


def verify_registration_data(category, email, username, first_name, last_name, password, confirm_password,
                             address):

    if not verify_input_data(**dict(category=category, email=email, username=username,
                                    first_name=first_name, last_name=last_name,
                                    password=password, confirm_password=confirm_password,
                                    address=address)):
        return dict(message='Invalid data format. Check email field and fill in all fields.', status_code=400)


def sign_up(**data):
    if data['password'] == data['confirm_password']:
        new_user = False
        if data['category'] == 'user':
            new_user = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'],
                            username=data['username'], password=data['password'], address=data['address']).add_user()
            tag = "User"
        elif data['category'] == 'caterer':
            new_user = Caterer(first_name=data['first_name'], last_name=data['last_name'], email=data['email'],
                               username=data['username'], password=data['password'],
                               address=data['address']).add_caterer()
            tag = "Caterer"
        else:
            return dict(message='category can either be user or caterer.', status_code=400)

        if new_user:
            return dict(message='{} {} successfully signed up.'.format(tag, data['username']), status_code=201)
        else:
            return dict(message='{} {} already exists.'.format(tag, data['username']), status_code=403)

    else:
        return dict(message='Passwords don\'t match.', status_code=400)


def log_in(**data):
    if data['category'] == 'user':
        user_info = User.get_user(data['username'])

    elif data['category'] == 'caterer':
        user_info = Caterer.get_caterer(data['username'])

    if user_info:
        token = verify_password(username=user_info.username, user_email=user_info.email, db_password=user_info.password,
                                input_password=data['password'], category=data['category'])
        if token:
            return dict(token=token, status_code=200, operation=True)

    return dict(message='Invalid Username or Password', status_code=401, operation=False)






