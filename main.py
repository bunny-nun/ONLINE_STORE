from flask import Flask, request, render_template
import logging

app = Flask(__name__)
app.secret_key = b'382f6e6456a59eb1cade6c54d6c696a39f44b062c440a396ef35563013a86477'
logger = logging.getLogger(__name__)


def header_menu():
    menu = [{'title': "Главная", 'url': '/'},
            {'title': "Блузки и рубашки", 'url': '/top/'},
            {'title': "Брюки", 'url': '/pants/'},
            {'title': "Обувь", 'url': '/shoes/'},
            {'title': "Контакты", 'url': '/contacts/'}]
    return menu


@app.route('/')
def index():
    context = {'menu': header_menu(),
               'title': 'Главная',
               'cur_url': '/'}
    return render_template('index.html', **context)


@app.route('/top/')
def top():
    context = {'menu': header_menu(),
               'title': 'Блузки и рубашки',
               'cur_url': '/top/'}
    return render_template('top.html', **context)


@app.route('/pants/')
def pants():
    context = {'menu': header_menu(),
               'title': 'Брюки',
               'cur_url': '/pants/'}
    return render_template('pants.html', **context)


@app.route('/shoes/')
def shoes():
    context = {'menu': header_menu(),
               'title': 'Обувь',
               'cur_url': '/shoes/'}
    return render_template('shoes.html', **context)


@app.route('/contacts/')
def contacts():
    context = {'menu': header_menu(),
               'title': 'Контакты',
               'cur_url': '/contacts/'}
    return render_template('contacts.html', **context)


@app.errorhandler(404)
def page_not_found(e):
    logger.warning(e)
    context = {'menu': header_menu(),
               'title': 'Страница не найдена',
               'url': request.base_url}
    return render_template('404.html', **context), 404


if __name__ == '__main__':
    app.run(debug=True)
