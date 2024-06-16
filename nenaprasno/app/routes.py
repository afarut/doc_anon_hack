from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import RegistrationForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, Texts
from datetime import timedelta
from docx import Document
from PyPDF2 import PdfReader
import io
from werkzeug.utils import secure_filename
import os
from PIL import Image
import pytesseract
from app.get_api_key import get_iam_token
import requests

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = Users.query.filter_by(login=form.login.data).first()
        if existing_user is None:
            user = Users(login=form.login.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        else:
            flash('Login already exists. Please use a different login.')
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid login or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data, duration=timedelta(weeks=1))
        return redirect(url_for('profile'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    page = request.args.get('page', 1, type=int)
    per_page = 3
    pagination = Texts.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=per_page, error_out=False)
    user_texts = pagination.items

    return render_template('profile.html', texts=user_texts, pagination=pagination)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    headers = {
    'x-node-id': 'bt1kip69f5oa5jkv1pk0',
    'Authorization': f'Bearer {get_iam_token()["iamToken"]}',
    'x-folder-id': 'b1g209sjmeesb972og4q',
    }
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        title = request.form['title']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            if filename.endswith('docx'):
                content = extract_text_from_docx(filepath)
            elif filename.endswith('pdf'):
                content = extract_text_from_pdf(filepath)
            elif filename.endswith('jpg') or filename.endswith('jpeg'):
                image = Image.open(filepath)
                content = pytesseract.image_to_string(image, lang='rus')
            elif filename.endswith('png'):
                image = Image.open(filepath)
                content = pytesseract.image_to_string(image, lang='rus')
            else:
                flash('File format not supported')
                return redirect(request.url)
            result_text = ""
            for i in get_chuncks(str(content)):
                json_data = {
                    'text': i,
                }
                response = requests.post('https://node-api.datasphere.yandexcloud.net', headers=headers, json=json_data)
                result_text += response.json()["result"].encode('utf-8').decode()
            new_text = Texts(user_id=current_user.id, title=title, content=result_text)
            db.session.add(new_text)
            db.session.commit()
            flash('File uploaded and text extracted successfully!')
            return redirect(url_for('profile'))
    
    return render_template('upload.html', title='Upload File')

def get_chuncks(string):
    result = []
    for i in range(len(string) // 512 + (len(string) % 512 != 0)):
        result.append(string[i*512:(i+1) * 512])
    return result

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_docx(filepath):
    doc = Document(filepath)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

def extract_text_from_pdf(filepath):
    pdf = PdfReader(filepath)
    num_pages = len(pdf.pages)
    text = ""

    for page_num in range(num_pages):
        page = pdf.pages[page_num]
        if '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].get_object()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    base64_data = xObject[obj]._data
                    image = Image.open(io.BytesIO(base64_data))
                    page_text = pytesseract.image_to_string(image, lang='rus')
                    text += page_text + "\n"
    return text

@app.route('/delete_text/<int:text_id>', methods=['POST'])
@login_required
def delete_text(text_id):
    text = Texts.query.get_or_404(text_id)
    if text.author != current_user:
        return redirect(url_for('profile'))
    db.session.delete(text)
    db.session.commit()
    flash('Text deleted successfully!')
    return redirect(url_for('profile'))
