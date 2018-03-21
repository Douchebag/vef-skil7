from bottle import run, route, template, request, response, redirect, static_file, error

'''
@route('/')
def index():
    if request.get_cookie("hello"):
        return "hello again"
    else:
        response.set_cookie("hello", "world")
        return "hello world"
'''

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

@route("/static/<filename>")
def server_static(filename):
    return static_file(filename, root='./files')

@error(404)
def error404(error):
    return "<h1>Þessi síða fannst ekki</h1><br><a href='/'>Heim</a>"

#https://codepen.io/Lewitje/pen/BNNJjo
run()