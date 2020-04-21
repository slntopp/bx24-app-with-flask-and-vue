from flask import Flask, request
from functools import wraps

def return_200_if_HEAD(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if request.method == 'HEAD': return '', 200
        return f(args, kwargs)
    return wrap

app = Flask(__name__, template_folder='public')

#Configuration of application, see configuration.py, choose one and uncomment.
app.config.from_object('app.conf.Config')

# db = SQLAlchemy(app)

from app import routes#, models

# db.create_all()