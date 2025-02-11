from flask import Flask, render_template, request, redirect, url_for, make_response, session

app = Flask(__name__)
app.secret_key = 'chave-secreta'

usuarios_registrados = []

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nome = request.form['nome']

        for usuario in usuarios_registrados:
            if usuario['username'] == username:
                return render_template('cadastro.html', erro="Usuário já cadastrado.")
        
        usuarios_registrados.append({'username':username, 'password':password, 'nome':nome})
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for usuario in usuarios_registrados:
            if usuario['username'] == username and usuario['password'] == password:
                session['username'] = username
                resposta = make_response(redirect(url_for('dashboard')))
                resposta.set_cookie('username', username, max_age=60*60*24)
                return resposta

        if username == 'admin' and password == 'senha123':
            session['username'] = username
            resposta = make_response(redirect(url_for('dashboard')))
            resposta.set_cookie('username', username, max_age=60*60*24)
            return resposta
        
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos.')
        
    if 'username' in session: 
        return redirect(url_for('dashboard'))
        
    
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login.html'))
    
    return render_template('dashboard.html', username=username)

@app.route('/logout', methods= ['POST'])
def logout():
    session.pop('username', None)

    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username','',max_age=0)
    return resposta

@app.route('/usuarios')
def listar_usuarios():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('usuarios.html', usuarios=usuarios_registrados)