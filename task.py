from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import sqlite3

app = Flask(__name__)
api = Api(app)


conn = sqlite3.connect('test.db',check_same_thread=False)
cursor = conn.cursor()
with conn:
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (message_id INTEGER PRIMARY KEY, data TEXT)")

def abort_if_message_doesnt_exist(message_id):
    cursor.execute("SELECT message_id FRom messages where message_id=:ms_id",{"ms_id":message_id})
    mssg = cursor.fetchone()
    if not mssg:
        abort(404, message="Message {} doesn't exist".format(message_id))

parser = reqparse.RequestParser()
parser.add_argument('data')


# Message
# shows a single message item and delete,update a message item
class Message(Resource):
    def get(self, message_id):
        abort_if_message_doesnt_exist(message_id)
        cursor.execute("SELECT * FROM messages where message_id=:ms_id",{"ms_id":message_id})
        mssg = cursor.fetchall()
        return dict(mssg)

    def delete(self, message_id):
        abort_if_message_doesnt_exist(message_id)
        with conn:
            cursor.execute("DELETE FROM messages WHERE message_id=:ms_id",{'ms_id':message_id})
        return '', 204

    def put(self, message_id):
        args = parser.parse_args()
        data = args['data']
        with conn:
            cursor.execute("UPDATE messages SET data=:data WHERE message_id=:ms_id",{"ms_id":message_id, 'data':data})
        return {'data': data}, 201


# MessageList
# shows a list of all messages, and POST to add new datas
class MessageList(Resource):
    def get(self):
        cursor.execute("SELECT * FROM messages")
        mssg = cursor.fetchall()
        return dict(mssg)

    def post(self):
        args = parser.parse_args()
        with conn:
            cursor.execute("INSERT INTO messages (data) VALUES (:data)",{'data':args['data']})
        cursor.execute("SELECT * FROM messages where message_id=last_insert_rowid()")
        mssg = cursor.fetchall()
        return dict(mssg), 201

##
## setup the Api resource routing.
##
api.add_resource(MessageList, '/messages')
api.add_resource(Message, '/messages/<message_id>')


if __name__ == '__main__':
    app.run(debug=True)