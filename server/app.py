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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
  if request.method == 'GET':
    #GET ALL THE MESSAGES FROM DATABASE
    #LOOP THROUGH AND CALL THE .to_dict()method on each object
    messages = [message.to_dict() for message in Message.query.all()]
    #create a response with make_response
    response = make_response(messages, 200)
    #return the response
    return response
  elif request.method == 'POST':
    front_data = request.get_json()
    new_message = Message(
       body = front_data.get("body"),
       username = front_data.get("username")
    )
    db.session.add(new_message)
    db.session.commit()
    response = make_response(new_message.to_dict(), 201)
    return response
      
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
  message = Message.query.filter(Message.id == id).first()

  if request.method == 'PATCH':
    print('here')
    data = request.get_json()
    for attr in data:
      setattr(message, attr, data[attr])
    #print(message.body)
    db.session.add(message)
    db.session.commit()
    return make_response(message.to_dict(), 200)
  
  if request.method == 'DELETE':
    #delete message from database
    db.session.delete(message)
    db.session.commit()
    #create response
    response = {
      "delete_successful": True,
      "message": "Message deleted."
    }
    #return response
    return make_response(response, 200)


if __name__ == '__main__':
    app.run(port=5555)
