#!/usr/bin/python3
"""api module"""

from models import storage
from api.v1.views import app_view
from flask import Flask

app = Flask(__name__)

app.register_blueprint(app_view)

@app.teardown_appcontext
def tear_down():
    storage.close()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)