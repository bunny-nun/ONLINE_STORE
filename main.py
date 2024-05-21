from flask import Flask
from flask import render_template

app = Flask(__name__)


def header_menu():
    menu = [{'title': "Главная", 'url': '/'},
            {'title': "Блузки и рубашки", 'url': '/top/'},
            {'title': "Брюки", 'url': '/pants/'},
            {'title': "Обувь", 'url': '/shoes/'},
            {'title': "Контакты", 'url': '/contacts/'}]
    return menu


@app.route('/')
def index():
    context = {'menu': header_menu(), 'title': 'Главная', 'cur_url': '/'}
    return render_template('index_2.html', **context)


@app.route('/top/')
def top():
    context = {'menu': header_menu(), 'title': 'Блузки и рубашки',
               'cur_url': '/top/'}
    return render_template('top.html', **context)


@app.route('/pants/')
def pants():
    context = {'menu': header_menu(), 'title': 'Брюки',
               'cur_url': '/pants/'}
    return render_template('pants.html', **context)


@app.route('/shoes/')
def shoes():
    context = {'menu': header_menu(), 'title': 'Обувь',
               'cur_url': '/shoes/'}
    return render_template('shoes.html', **context)


@app.route('/contacts/')
def contacts():
    context = {'menu': header_menu(), 'title': 'Контакты',
               'cur_url': '/contacts/'}
    return render_template('contacts.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
