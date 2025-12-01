from flask import render_template,request,Blueprint,session

pages = Blueprint('pages',__name__, url_prefix='/', template_folder="../templates",)

@pages.route('/')
def index():
    user_id = session.get('user_id')
    return render_template('index.html',user_id=user_id)

@pages.route('/register',methods=['GET','POST'])
def register():
    return render_template('register.html')

@pages.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')    

@pages.route('/events',methods=['GET'])
def event_page():
    user_id = session.get('user_id')
    return render_template('events.html',user_id=user_id)

@pages.route('/payment',methods=['GET'])
def payment_page():
    return render_template('payment.html')


# admin routes
@pages.route('/admin',methods=['GET'])
def admin_dashboard():
    return render_template('admin.html',is_admin = True)

@pages.route('/admin/events',methods=['GET'])
def admin_events_page():
    return render_template('admin_events.html',is_admin = True)

@pages.route('/admin/events-create',methods=['GET','POST'])
def admin_events_create_page():
    return render_template('event_create.html',is_admin = True)

@pages.route('/admin/users',methods=['GET'])
def admin_users_page():
    return render_template('admin_users.html',is_admin = True , user_id =session.get('user_id'))

@pages.route('/admin/payments',methods=['GET'])
def admin_payments_page():
    path = request.args.get('path','')
    return render_template('admin_payments.html',is_admin = True , path=path)