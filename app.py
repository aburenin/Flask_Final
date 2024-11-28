import datetime
import os
import requests
from werkzeug import urls

from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, make_response, request, jsonify, abort
from flask import redirect, url_for, flash, Response, send_file
from flask_assets import Environment, Bundle

from flask_cors import CORS
from flask_login import LoginManager, logout_user, login_user, login_required, current_user
from flask_mail import Mail, Message

from Datenschutz import Datenschutz
from Models import db, bcrypt
from Path import UserDirectories
from Question import Question
from Preise import Preise
from Client import Client, GetClient, ProjectManager
from Proof import ProjectProof
from portfolio import Portfolio
from Support import EmailSender
from adminka_support import get_client_data, upload_files

from config import alt_tags_newborn, alt_tags_babybauch, alt_tags_baby

# from support_functions import key_number


app = Flask(__name__)
app.config.from_object('config')

bcrypt.init_app(app)
db.init_app(app)
# mail = Mail(app)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

assets = Environment(app)

# Генерация путей к CSS-файлам
css = Bundle(
    os.path.join('css', 'reset.css'),
    os.path.join('css', 'main.css'),
    os.path.join('css', 'footer.css'),
    os.path.join('css', 'navbar.css'),
    os.path.join('css', 'modal.css'),
    os.path.join('css', 'carousel_main.css'),
    os.path.join('css', 'FAQ.css'),
    output=os.path.join('css', 'styles.css'),
    filters='cssmin'
)
# Объединение и минимизация CSS файлов
# css = Bundle('css/reset.css', 'css/main.css', 'css/footer.css', 'css/navbar.css',
#              'css/modal.css', 'css/carousel_main.css', 'css/FAQ.css', output='css/styles.css', filters='cssmin')
assets.register('css_all', css)

with app.app_context():
    assets._named_bundles['css_all'].urls()


@login_manager.user_loader
def load_user(user_id):
    return GetClient.filter_by(app=app, id=user_id)


CORS(app=app)

# from flask_caching import Cache
#
# cache = Cache(app, config={
#     'CACHE_TYPE': 'simple'
# })


load_dotenv(find_dotenv())

# clear_portfolio_html()
Portfolio.Gallery.clear()

# Create new Data Base if not exist and check for changed elements
if not os.path.exists('instance/fotos-baby.db'):
    with app.app_context():
        db.create_all()
Preise.check_db(app=app)
Question.check_db(app=app)


@app.route('/')
def index():
    questions = Question.query.all()
    response = make_response(render_template('index.html', questions=questions), 200)
    return response


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


@app.route('/kontakt/', methods=['GET', 'POST'])
def kontakt():
    if request.method == 'POST':
        turnstile_token = request.form.get("cf-turnstile-response")
        if not turnstile_token:
            return jsonify({"success": False, "message": "CAPTCHA token missing, please reload page!"}), 400

        # Проверка токена через API Cloudflare
        payload = {"secret": os.getenv('SECRET_KEY'), "response": turnstile_token}
        verify_response = requests.post(os.getenv('VERIFY_URL'), data=payload).json()


        if not verify_response.get("success"):
            return jsonify({"success": False, "message": "CAPTCHA verification failed, please reload page!"}), 403


        if verify_response.get("success"):
            try:
                mail = EmailSender(app)
                mail.send(app)
                print('200')
                return jsonify({"status": "success"}), 200
            except:
                print('400')
                return jsonify({"status": "failure"}), 400
    if request.method == 'GET':
        response = make_response(render_template('kontakt.html', site_key=os.getenv('SITE_KEY')),
                                 200)
        return response


@app.route('/portfolio-<category>/', endpoint='portfolio')
def portfolio_gallery(category):
    if category not in ['newborn', 'babybauch', 'baby']:
        abort(404)
    alt_tags: list[str] = []
    match category:
        case 'newborn':
            alt_tags = alt_tags_newborn
        case 'babybauch':
            alt_tags = alt_tags_babybauch
        case 'baby':
            alt_tags = alt_tags_baby
    response = Portfolio.Gallery.create(category, alt_tags)
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
        user = GetClient.filter_by(app=app, name=login)

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


@app.route('/about_me/')
def about():
    response = make_response(render_template('about.html'), 200)
    return response


@app.route('/contact-me/')
def contactMe():
    response = render_template('/modals/contact_me.html')
    return response


@app.route('/success/')
def success():
    text = request.args.get('text')
    client = GetClient.filter_by(app=app, id=request.args.get('clientID'))
    action = request.args.get('action')
    response = render_template('/modals/success.html', text=text, client=client, action=action)
    return response


@app.route('/datenschutz/')
def datenschutz():
    text = Datenschutz.parser()
    response = make_response(render_template('datenschutz.html', text=text, date=datetime.date.today()), 200)
    return response



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/adminka/', methods=['GET', 'POST', 'DELETE'])
# @login_required
def adminka():
    if request.method == 'GET':
        if request.args.get('project'):
            client = request.args.get('project')
            project = ProjectProof(client)
            response = project.get_html_for_gallery()
            return make_response(render_template('project.html', projectName=client, gallery=response), 200)
        response = make_response(render_template('adminka.html'), 200)
        return response
    if request.method == 'POST':
        match request.args.get('action'):

            case 'getClients':
                response = get_client_data()
                return response

            case 'addNew':
                status = ProjectManager.add_new(app, request.form.get('projectName'))
                return jsonify(status)

            case 'chngPassw':
                project_name = request.form.get('projectName')
                new_passw = request.form.get('projectPassword')
                status = ProjectManager.change_password(app, name=project_name, psw=new_passw)
                return jsonify(status)

            case 'addFotoToProject':
                uploaded_file = request.files.get('file')
                projectName = request.args.get('projectName')
                status = upload_files(uploaded_file=uploaded_file, projectName=projectName)
                return jsonify(status)

            case 'clearGallery':
                projectName = request.args.get('projectName')
                status = UserDirectories(projectName).clear_gallery()
                return jsonify(status)

    if request.method == 'DELETE':
        client = GetClient.filter_by(app, id=request.form.get('id'))

        match request.form.get('action_type'):

            case 'delProject':
                response = ProjectManager.delete(app, client)
                return response
            case 'clearFotoList':
                response = client.clear_foto_list(app)
                return response

        match request.get_json().get('action'):
            case 'delFoto':
                projectname = request.get_json().get('projectName')
                filename = request.get_json().get('fileName')
                # ----  return никак не обрабатывается сейчас на фронте....
                return UserDirectories(projectname).delete_img_from_gallery(fileName=filename)


@app.route('/client-gallery/<username>', methods=['GET', 'POST', 'DELETE'])
# @login_required
def client_gallery(username):
    """Function to work with client gallery: check approved photos, add photo to DB,
    remove photo from DB, download all photos from gallery"""
    project = ProjectProof(username)

    match request.args.get('action'):

        case 'checkApprovedImages':
            files = project.approved_images(app)
            try:
                return jsonify(files)
            except Exception as e:
                return jsonify({'error': str(e)})

        case 'addToDB':
            response = project.add_image_to_db(app)
            return jsonify(response)

        case 'delFromDB':
            response = project.remove_image_from_db(app)
            return jsonify(response)

        case 'download':
            zipFile = project.download_client_gallery()
            return send_file(zipFile, as_attachment=True)

    response = project.get_html_for_gallery()

    picture = project.main_pic()

    return make_response(render_template('client.html', projectName=username, gallery=response, picture=picture), 200)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3000, debug=True)
