from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
api = Api(app)

conn = sqlite3.connect('data.db',check_same_thread=False)
cursor = conn.cursor()
with conn:
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                                message_id INTEGER PRIMARY KEY,
                                created_at TIMESTAMP DEFAULT current_timestamp,
                                data TEXT
                                )"""
                    )
# returns True if palindrome
def isPal(message):
    return message == message[::-1]

def abort_if_message_doesnt_exist(message_id):
    cursor.execute("SELECT message_id FROM messages WHERE message_id=:ms_id",{"ms_id":message_id})
    mssg = cursor.fetchone()
    if not mssg:
        abort(404, message="Message {} doesn't exist".format(message_id))

parser = reqparse.RequestParser()
parser.add_argument('data')
parser.add_argument('page')


# Message
# shows a single message item and delete,update a message item
class Message(Resource):
    def get(self, message_id):
        abort_if_message_doesnt_exist(message_id)
        cursor.execute("SELECT message_id , data FROM messages where message_id=:ms_id",{"ms_id":message_id})
        mssg = cursor.fetchall()
        return {'data' : {
			'messageId' : mssg[0][0],
			'message' : mssg[0][1],
			'isPalindrome' : isPal(str(mssg[0][1])) }
		} ,200

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
        return {'data': {
			'messageId' : message_id,
			'message' : data}
		}, 201

# MessageList
# shows a list of all messages, and POST to add new data
class MessageList(Resource):
    def get(self):
        OFT = 0
        LMT = 10
        args = parser.parse_args()
        if args['page'] is not None:
            OFT = LMT * int(args['page'])
        cursor.execute("""
                        SELECT message_id , data , (SELECT COUNT(*) FROM messages) count
                        FROM messages
                        ORDER BY created_at DESC
                        LIMIT :lmt
                        OFFSET :oft """,
                        {'lmt':LMT, 'oft':OFT})
        mssg = cursor.fetchall()
	count = mssg[0][2] if mssg != []  else 0
	print count, 'count'
        lst = []
        for i in mssg:
            lst.append({ 'messageId': i[0], 'message' : i[1]})
        return { 'data' : lst, 'count' : count}

    def post(self):
        args = parser.parse_args()
        with conn:
            cursor.execute("INSERT INTO messages (data) VALUES (:data)",{'data':args['data']})
        cursor.execute("SELECT message_id , data FROM messages where message_id=last_insert_rowid()")
        mssg = cursor.fetchall()
        mesgId = mssg[0][0]
        data = mssg[0][1]
        return { 'messageId' : mesgId , 'message' : data}, 201

##
## setup the Api resource routing.
##
api.add_resource(MessageList, '/api/messages')
api.add_resource(Message, '/api/messages/<message_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
