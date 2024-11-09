import datetime
import os
from argparse import Action

from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, make_response, request, jsonify, abort, redirect, url_for, flash, Response, send_file
from flask_assets import Environment, Bundle
# from flask_caching import Cache
from flask_cors import CORS
from flask_login import LoginManager, logout_user, login_user, login_required, current_user
from sqlalchemy.sql.dml import ReturningDelete

from Models import db, Client, Question, Preise, UserDirectories
from adminka_support import get_client_data, create_paths, delete_project_path, upload_files, clear_client_gallery
from adminka_support import get_html_for_gallery, delete_img_from_gallery, delete_project, clear_foto_list
from config import alt_tags_newborn, alt_tags_babybauch, alt_tags_baby
from support_functions import get_html_for_portfolio, parser_datenschutz, clear_portfolio_html
from proofing_gallery_support import check_approved_imges, add_image_to_db, remove_image_from_db, check_main_picture
from proofing_gallery_support import download_client_gallery

from werkzeug import urls

# from flask_mail import Mail, Message
# from flask_socketio import SocketIO

# eventlet.monkey_patch()

app = Flask(__name__)
app.config.from_object('config')


# bcrypt.init_app(app)

db.init_app(app)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

assets = Environment(app)

# Объединение и минимизация CSS файлов
css = Bundle('css/reset.css', 'css/main.css', 'css/footer.css', 'css/navbar.css',
             'css/modal.css', 'css/carousel_main.css', 'css/FAQ.css', output='css/styles.css', filters='cssmin')
assets.register('css_all', css)


@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))


CORS(app=app)

#
# cache = Cache(app, config={
#     'CACHE_TYPE': 'simple'
# })


load_dotenv(find_dotenv())
clear_portfolio_html()

# # Create new Data Base if not exist.
if not os.path.exists('instance/fotos-baby.db'):
   with app.app_context():
        db.create_all()
Preise.check_db(app=app)
Question.checkDB(app=app)

@app.route('/')
def index():
    questions = Question.query.all()
    response = make_response(render_template('index.html', questions=questions), 200)
    return response


# @app.route('/faq/')
# def faq():
#     questions = db.session.query(Question).all()
#     response = render_template('/modals/FAQ.html', questions=questions)
#     return response


@app.route('/preise/')
def prices():
    match request.args.get('action'):
        case 'getPrices':
            prices_array = []
            prices = Preise.query.all()
            for price in prices:
                prices_array.append({'name': price.name,
                                     'description': price.description.split('|'),
                                     'price': price.price})
            response = jsonify(prices_array)
            return response
    response = make_response(render_template('preise.html'), 200)
    return response


@app.route('/kontakt/')
def kontakt():
    response = make_response(render_template('kontakt.html'), 200)
    return response


@app.route('/portfolio-<category>/', endpoint='portfolio')
def portfolio_gallery(category):
    if category not in ['newborn', 'babybauch', 'baby']:
        abort(404)
    match category:
        case 'newborn':
            alt_tags = alt_tags_newborn
        case 'babybauch':
            alt_tags = alt_tags_babybauch
        case 'baby':
            alt_tags = alt_tags_baby
    response = get_html_for_portfolio(category, alt_tags)
    response = make_response(
        render_template('portfolio_gallery.html', category=category, gallery=response), 200)
    return response


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        if current_user.name == 'adminka':
            return redirect(url_for('adminka'))
        return f"Hello {current_user.name}"

    login = request.form.get('login')
    password = request.form.get('password')
    next_url = request.args.get("next")
    if login and password:
        user = Client.query.filter_by(name=login).first()

        if user:
            login_user(user)
            if next_url and urls.url_parse(next_url).netloc == '':
                return redirect(next_url)
            elif user.name == 'adminka':
                return redirect(url_for('adminka'))
            else:
                return redirect(url_for('default_route'))  # Замените на нужный маршрут
        else:
            flash('Неверные учетные данные', 'warning')
    response = make_response(render_template('login.html'), 200)
    return response


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/impressum/')
def impressum():
    response = render_template('/modals/impressum.html')
    return response


@app.route('/contact-me/')
def contactMe():
    response = render_template('/modals/contact_me.html')
    return response


@app.route('/success/')
def success():
    text = request.args.get('text')
    client = Client.query.filter_by(id=request.args.get('clientID')).first()
    action = request.args.get('action')
    response = render_template('/modals/success.html', text=text, client=client, action=action)
    return response


@app.route('/datenschutz/')
def datenschutz():
    text = parser_datenschutz()
    response = make_response(render_template('datenschutz.html', text=text, date=datetime.date.today()), 200)
    return response


@app.route('/adminka/', methods=['GET', 'POST', 'DELETE'])
# @login_required
def adminka():
    projectName = request.args.get('projectName')
    if request.method == 'GET':
        if request.args.get('project'):
            project = request.args.get('project')
            response = get_html_for_gallery(project)
            return make_response(render_template('project.html', projectName=project, gallery=response), 200)
        response = make_response(render_template('adminka.html'), 200)
        return response
    if request.method == 'POST':
        match request.args.get('action'):

            case 'getClients':
                response = get_client_data()
                return response

            case 'addNew':
                projectName = request.form.get('projectName')
                # status = add_new_project(app)
                status = Client.add_new_project(app)
                create_paths(projectName)
                return jsonify(status)

            case 'chngPassw':
                # status = change_project_password(app)
                status = Client.change_project_password(app)
                return jsonify(status)

            case 'addFotoToProject':
                uploaded_file = request.files.get('file')
                status = upload_files(uploaded_file=uploaded_file, projectName=projectName)
                return jsonify(status)

            case 'clearGallery':
                status = clear_client_gallery(projectName)
                return jsonify(status)
    if request.method == 'DELETE':
        match request.form.get('action_type'):
            case 'delProject':
                response = delete_project(app, id=request.form.get('id'))
                return response
            case 'clearFotoList':
                response = clear_foto_list(app, id=request.form.get('id'))
                return response

        match request.get_json().get('action'):
            case 'delFoto':
                projectName = request.get_json().get('projectName')
                fileName = request.get_json().get('fileName')
                delete_img_from_gallery(projectName, fileName)
                return Response(status=200)




@app.route('/project_delete/<int:id>/', methods=['DELETE'])
# @login_required
def project_delete(id):
    if current_user.name == 'adminka':
        try:
            project = Client.query.filter_by(id=id).first()

            db.session.delete(project)
            db.session.commit()

            if delete_project_path(project.name) == False:
                response = Response(render_template('/hilfsportal/alert.html', status='warning',
                                                    text=f"Невозможно удалить содержимое рроекта {project.name}. Обратитесь к администратору."))
                response.headers['X-Success'] = 'warning'
                return response

            response = Response(
                render_template('/hilfsportal/alert.html', status='success', text=f"Проект {project.name} был удален."))
            response.headers['X-Success'] = 'success'
        except Exception as e:
            response = Response(render_template('/hilfsportal/alert.html', status='warning', text=f"{e}"))
            response.headers['X-Success'] = 'warning'
    return response


@app.route('/client-gallery/<username>', methods=['GET', 'POST', 'DELETE'])
# @login_required
def client_gallery(username):

    match request.args.get('action'):

        case 'checkApprovedImages':
            files = check_approved_imges(app, username)
            try:
                return jsonify(files)
            except Exception as e:
                return jsonify({'error': str(e)})

        case 'addToDB':
            response = add_image_to_db(app, username)
            return jsonify(response)

        case 'delFromDB':
            response = remove_image_from_db(app, username)
            return jsonify(response)

        case 'download':
            zipFile = download_client_gallery(username)
            print(zipFile)
            return send_file(zipFile, as_attachment=True)
#
#     case 'loadPictures':
#         response = get_html_for_gallery(username)
#         return response

    # project = request.args.get('project')
    response = get_html_for_gallery(username)
    picture = check_main_picture(username)
    return make_response(render_template('client.html', projectName=username, gallery=response, picture=picture), 200)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
