# importing the Flask object from the flask module
# (that we installed with pip3 install flask)
from flask import Flask

# instantiating the flask app 
app = Flask(__name__)

# register home route (/) to app
@app.route("/")
def hello_world():
    """ 
    return hello world to user 
    """
    return "<p>Hello, World!</p>"

# run app on port 5000
app.run(port=5000)