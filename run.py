from app.v1.views.meals import meals
from app.v1.views.menu import menu
from app.v1.views.users import users
from flasgger import Swagger
from flask import Flask

from app.v1.views.orders import orders


app = Flask(__name__, instance_relative_config=True)

swagger = Swagger(app)

app.register_blueprint(users)

app.register_blueprint(meals)

app.register_blueprint(menu)

app.register_blueprint(orders)


if __name__ == '__main__':
    app.run(debug=True)