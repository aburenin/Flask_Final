import datetime
import os
from urllib.parse import urlparse

import requests
from flask import render_template, make_response, request, jsonify, abort
from flask import redirect, url_for, flash, send_file
from flask_login import logout_user, login_user, login_required, current_user

from Client import GetClient, ProjectManager
from Datenschutz import Datenschutz
from Path import UserDirectories
from Preise import Preise
from Proof import ProjectProof
from Question import Question
from Support import EmailSender
from adminka_support import get_client_data, upload_files
from portfolio.Portfolio import Gallery

from app_init import app

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
            for price in Preise.query.all():
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
                # print('200')
                return jsonify({"status": "success"}), 200
            except:
                # print('400')
                return jsonify({"status": "failure"}), 400
    if request.method == 'GET':
        response = make_response(render_template('kontakt.html', site_key=os.getenv('SITE_KEY')),
                                 200)
        return response


@app.route('/portfolio-<category>/', endpoint='portfolio')
def portfolio_gallery(category: str):
    if category not in ['newborn', 'babybauch', 'baby']:
        return abort(404)
    else:
        response = Gallery(category).create()
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
        user = GetClient(app=app).filter_by(name=login)

        if user:
            login_user(user)

            if next_url and urlparse(next_url).netloc == '':
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
    client = GetClient(app=app).filter_by(id=request.args.get('clientID'))
    action = request.args.get('action')
    response = render_template('/modals/success.html', text=text, client=client, action=action)
    return response


@app.route('/datenschutz/')
def datenschutz():
    daten = Datenschutz()
    response = make_response(render_template('datenschutz.html', text=daten.text, date=datetime.date.today()), 200)
    return response


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/adminka/', methods=['GET', 'POST', 'DELETE'])
@login_required
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
                status = ProjectManager(app=app).add_new(project_name=request.form.get('projectName'))
                return jsonify(status)

            case 'chngPassw':
                project_name = request.form.get('projectName')
                new_passw = request.form.get('projectPassword')
                status = ProjectManager(app=app).change_password(name=project_name, psw=new_passw)
                return jsonify(status)

            case 'addFotoToProject':
                uploaded_file = request.files.get('file')
                projectName = request.args.get('projectName')
                status = upload_files(uploaded_file=uploaded_file, projectname=projectName)
                return jsonify(status)

            case 'clearGallery':
                projectName = request.args.get('projectName')
                status = UserDirectories(username=projectName).clear_gallery()
                return jsonify(status)

    if request.method == 'DELETE':
        client = GetClient(app=app).filter_by(id=request.form.get('id'))

        match request.form.get('action_type'):

            case 'delProject':
                response = ProjectManager(app=app).delete(client)
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

    return make_response(render_template('client.html',
                                         projectName=username, gallery=response, picture=project.mainpic), 200)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3000, debug=True)
