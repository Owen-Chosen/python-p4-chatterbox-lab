from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Hi, I\'M OWEN</h1>'

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    
    if request.method == 'GET':
        all_messages = []
        for message in Message.query.order_by((Message.created_at).asc()).all():
            all_messages.append(message.to_dict())
        return make_response(jsonify(all_messages), 200)
    
    elif request.method == 'POST':
        dict_of_message = request.get_json()
        new_message = Message(
            body = dict_of_message['body'],
            username = dict_of_message['username']
        )
        db.session.add(new_message)
        db.session.commit()

        return make_response(jsonify(new_message.to_dict()), 200)
    

@app.route('/messages/<int:id>', methods=['GET'])
def messages_by_id(id):
    
    if request.method == 'GET':
        message = Message.query.filter_by(id).first()
        return make_response(jsonify(message.to_dict()))
    elif request.method == 'PATCH':
        message = Message.query.filter_by(id).first()
        for attr in request.get_json():
            setattr(message, attr, request.get_json()[attr])
        db.session.add(message)
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)
    elif request.method == 'DELETE':
        message = Message.query.filter_by(id).first()
        db.session.delete(message)
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555)
