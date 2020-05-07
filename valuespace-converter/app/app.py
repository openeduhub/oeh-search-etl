from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from transform import Transform


# config
app = Flask(__name__)
app.secret_key = 'changethisinproduction'
api = Api(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Database

# Add Classes to API
api.add_resource(Transform, '/transform', methods=['POST'])


# Run app
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5010, debug=True)