import click
from flask import Flask, request, session, redirect, url_for, render_template
from flask_wtf.csrf import CSRFProtect
from models import db, User
from forms import RegisterForm
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = b'382f6e6456a59eb1cade6c54d6c696a39f44b062c440a396ef35563013a86477'
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Database created')


@app.cli.command('delete-user')
@click.argument('email')
def delete_user(email):
    user = User.query.filter_by(email=email).first()
    db.session.delete(user)
    db.session.commit()
    print(f'User with {email} has been deleted')


def header_menu():
    menu = [{'title': "Главная", 'url': '/'},
            {'title': "Блузки и рубашки", 'url': '#'},
            {'title': "Брюки", 'url': '#'},
            {'title': "Обувь", 'url': '#'},
            {'title': "Контакты", 'url': '#'}]
    return menu


@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        last_name = form.last_name.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='pbkdf2:sha256')

        session['name'] = name
        session['last_name'] = last_name
        session['email'] = email
        session['password'] = password

        user = User(name=name, last_name=last_name, email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()
        print(f'{user} added')
        return redirect(url_for('done'))

    context = {'menu': header_menu(),
               'title': 'Регистрация',
               'cur_url': '/register'}
    return render_template('register.html', **context,
                           form=form)


@app.route('/done')
def done():
    context = {'menu': header_menu(),
               'title': 'Регистрация завершена',
               'cur_url': '/done'}
    return render_template('done.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
