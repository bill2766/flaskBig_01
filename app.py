import json
import os
import uuid

from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session, jsonify
from flask_ckeditor import CKEditor, upload_success, upload_fail
from flask_dropzone import Dropzone
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError

from forms import UploadForm

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Custom config
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
if not os.path.exists(app.config['UPLOAD_PATH']):
    os.makedirs(app.config['UPLOAD_PATH'])
app.config['ALLOWED_EXTENSIONS'] = ['png']

# Flask-Dropzone config
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image'
app.config['DROPZONE_MAX_FILE_SIZE'] = 3
app.config['DROPZONE_MAX_FILES'] = 30
dropzone = Dropzone(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')

def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     img = request.files.get('photo')
#     filename = random_filename(img.filename)
#     img.save(os.path.join(app.config['UPLOAD_PATH'], filename))
#     session['filenames'] = [filename]
#     return redirect(url_for('show_images'))
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    img = request.files.get('photo')
    filename = random_filename(img.filename)
    img.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    img_url = "uploads/"+filename
    return jsonify({'success':200,"msg":"上传成功","img_url":img_url})

@app.route('/detectImg',methods=['POST'])
def detectImg():
    m = request.get_data()  # 获取字节流
    s1 = str(m, encoding='utf-8')  # 转换成字符串
    dic = json.loads(s1)  # 转换为字典
    imgSrc = dic['imgSrc']
    print(imgSrc)
    return jsonify({'success':200,"msg":"上传成功","value":imgSrc})

@app.route('/uploaded-images')
def show_images():
    return render_template('showImg_ex.html')

@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

# message flashing
@app.route('/flash')
def just_flash():
    flash('I am flash, who is looking for me?')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
