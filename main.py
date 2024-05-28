from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = b'382f6e6456a59eb1cade6c54d6c696a39f44b062c440a396ef35563013a86477'
app.session_cookie_secure = True


def header_menu():
    menu = [{'title': "Главная", 'url': '/'},
            {'title': "Блузки и рубашки", 'url': '#'},
            {'title': "Брюки", 'url': '#'},
            {'title': "Обувь", 'url': '#'},
            {'title': "Контакты", 'url': '#'}]
    return menu


@app.route('/')
def index():
    if 'name' in session:
        return redirect(url_for('welcome'))
    else:
        return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if name and email:
            session['name'] = name
            session['email'] = email
            return redirect(url_for('welcome'))
    context = {'menu': header_menu(),
               'title': 'Войти',
               'cur_url': '/login/'}
    return render_template('login.html', **context)


@app.route('/welcome/', methods=['GET', 'POST'])
def welcome():
    name = session.get('name')
    context = {'menu': header_menu(),
               'title': 'Добро пожаловать',
               'cur_url': '/login/',
               'name': name}
    return render_template('welcome.html', **context)


@app.route('/logout/', methods=['POST'])
def logout():
    session.pop('name', None)
    session.pop('email', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
