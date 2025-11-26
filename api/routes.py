from flask import Blueprint,request,jsonify,session
from extensions import db
import bcrypt
from schemas.user import User
from schemas.events import Event
from schemas.tickets import Ticket
from schemas.payment import Wallet,Transtions

api = Blueprint('api',__name__,url_prefix='/api')


@api.route('/')
def index():
    return "Hello, World!"

@api.route('/users',methods=['POST','GET','DELETE'])
def create_user():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    user = User.query.filter_by(email=data['email']).first()

    if user:
        return 'User already exists', 400
    
    salt = bcrypt.gensalt()
    data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), salt).decode('utf-8')

    user = User(**data)
    db.session.add(user)
    db.session.commit()

    user_wallet = {
            "user_id": user.id,
            "balance": 0.0
        }
    wallet = Wallet(**user_wallet)

    
    db.session.add(wallet)
    db.session.commit()
    return jsonify(user.to_dict())

@api.route('/users/<user_id>',methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message":"User not found"}),404
    
    wallet = Wallet.query.filter_by(user_id=user.id).first()
    if not wallet:
        return jsonify({"message":"Wallet not found"}),404
    
    db.session.delete(wallet)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message":"User deleted successfully"}),200

@api.route('/login',methods=['POST'])
def login_user():
    data = request.get_json()

    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password=password.encode('utf-8'), hashed_password=user.password.encode('utf-8')):
        return 'Invalid email or password', 401
    
    session['user_id'] = str(user.id)

    return jsonify(user.to_dict())

@api.route('/logout',methods=['POST'])
def logout_user():
    session.pop('user_id', None)
    return None

@api.route('/events', methods=['GET', 'POST'],strict_slashes=False)
def create_event():
    if request.method == 'GET':
        events = Event.query.all()
        return jsonify([event.to_dict() for event in events])
    data = request.get_json()
    print(data)
    event = Event(**data)
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict())

@api.route('/buy_ticket/<event_id>',methods=['POST'])
def buy_ticket(event_id):
    event = Event.query.get(event_id)
    
    user =User.query.get(request.get_json()['user_id'])
    
    if not event:
        return jsonify({"message":"Event not found"}),404
    
    if not user:
        return jsonify({"message":"User not found"}),404

    if event.avaiable_tickets <=0 or event.avaiable_tickets < request.get_json()['ticket']:
        return jsonify({"message":"No tickets available"}),400

    if user in event.users:
        return jsonify({"message":"User has already bought a ticket for this event"}),400

    event.avaiable_tickets -=1
    event.users.append(user)

    ticket = Ticket(
        user_id = user.id,
        event_id = event.id,
        total_token = request.get_json()['ticket']
    )
    db.session.add(ticket)
    db.session.commit()

    return event.to_dict()

@api.route('/tickets',methods=['GET'])
def get_tickets():
    tickets = Ticket.query.all()
    return [ticket.to_dict() for ticket in tickets]

@api.route('/get_user_ticket',methods=['GET'])
def get_user_ticket():
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({"message":"Unauthorized"}),401
    
    tickets = Ticket.query.filter_by(user_id=user_id).all()

    if not tickets:
        return jsonify([]),200
    return jsonify([ticket.to_dict() for ticket in tickets])

@api.route('/wallet',methods=['GET'])
def wallet_list():
    wallets = Wallet.query.all()
    return jsonify([wallet.to_dict() for wallet in wallets])

@api.route('/get_user_wallet/<user_id>',methods=['GET'])
def get_wallet(user_id:str):
    wallet = Wallet.query.filter_by(user_id = user_id).first()
    return jsonify(wallet.to_dict())

@api.route('/top_up_wallet',methods=['POST'])
def top_up():
    # user_id = session.get('user_id')
    # if not user_id:
    #     return jsonify({"message":"Unauthorized"}),401
    
    data = request.get_json()
    wallet = Wallet.query.filter_by(id = data['wallet_id']).first()

    if not wallet:
        return jsonify({"message":"Wallet not found"}),404
    
    transition = Transtions(**data)
    wallet.balance += data["amount"]
    db.session.add(transition)
    db.session.commit()
    return jsonify(wallet.to_dict())

@api.route('/transactions',methods=['GET'])
def get_transactions():
    transitions = Transtions.query.all()
    return jsonify([transition.to_dict() for transition in transitions])