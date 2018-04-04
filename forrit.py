#login form útlit frá https://codepen.io/Lewitje/pen/BNNJjo
from bottle import run, route, template, request, response, redirect, static_file, error, app
from beaker.middleware import SessionMiddleware

@route("/static/<filename>")
def server_static(filename):
    return static_file(filename, root='./files')

@error(404)
def error404(error):
    return "<h1>Þessi síða fannst ekki</h1><br><a href='/'>Heim</a>"

'''
@route('/')
def index():
    if request.get_cookie("hello"):
        return "hello again"
    else:
        response.set_cookie("hello", "world")
        return "hello world"
'''

#Login lausn - cookies
adminuser = 'admin'
adminpass = '12345'

@route('/')
def index():
    return template('index.tpl')

@route('/login')
def login():
    return template('login.tpl')

@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    if username == adminuser and password == adminpass:
        response.set_cookie("user", username, secret='AWDWd')
        return redirect('/restricted')
    else:
        return "Login failed. <br> <a href='/login'>Tilbaka</a>"

@route('/restricted')
def restricted():
    user = request.get_cookie("user", secret='AWDWd')
    #if user == adminuser:
    if user:
        return "Restricted area <br> <a href='/logout'>Log out</a>"
    else:
        return "Aðgangur bannaður"

@route('/logout')
def logout():
    response.set_cookie('user', "", expires=0)
    return "Þú hefur verið skráður út. <br> <a href='/login'>Login</a>"


#Session lausn

session_options = {
    'session.type': 'file',
    'session.data_dir': './data/'
}

my_session = SessionMiddleware(app(), session_options)

products = [
    {'pid': 1, 'name': 'Vara 1', 'price': 100},
    {'pid': 2, 'name': 'Vara 2', 'price': 400},
    {'pid': 3, 'name': 'Vara 3', 'price': 200},
    {'pid': 4, 'name': 'Vara 4', 'price': 800}
]

@route('/shop')
def shop():
    return template('shop.tpl', products=products)

@route('/cart/add/<id>')
def add_to_card(id):
    session = request.environ.get('beaker.session')
    session[id] = products[int(id)-1]['name']
    session.save()

    print(session)
    return redirect('/cart')

@route('/cart')
def cart():
    session = request.environ.get('beaker.session')
    karfa = []
    for i in range(len(products)+1):
        i = str(i)
        if session.get(i):
            vara = session.get(i)
            karfa.append(vara)

    return template('cart.tpl', karfa=karfa)
run(app=my_session, port=5000)