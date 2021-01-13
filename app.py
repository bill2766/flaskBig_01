import json
import os
import uuid

from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session, jsonify
from flask_ckeditor import CKEditor, upload_success, upload_fail
from flask_dropzone import Dropzone
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from caller import userTest

from forms import UploadForm

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Custom config
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
if not os.path.exists(app.config['UPLOAD_PATH']):
    os.makedirs(app.config['UPLOAD_PATH'])
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']
app.config['RESULT_PATH'] = os.path.join(app.root_path, 'resnet50/results_color_user_test')

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

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    img = request.files.get('photo')
    filename = random_filename(img.filename)
    img.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    img_url = "uploads/"+filename
    return jsonify({'success':200,"msg":"上传成功","img_url":img_url})

@app.route('/renet50/results_user_test/<path:filename>')
def get_result(filename):
    return send_from_directory(app.config['RESULT_PATH'], filename)

@app.route('/detectImg',methods=['POST'])
def detectImg():
    m = request.get_data()  # 获取字节流
    s1 = str(m, encoding='utf-8')  # 转换成字符串
    dic = json.loads(s1)  # 转换为字典
    imgSrc = dic['imgSrc']
    imgName = imgSrc.split("/")[1]
    # 调用模型进行图片处理
    result_filename = userTest(os.path.join(app.config['UPLOAD_PATH'], imgName))
    resultImgUrl = url_for('get_result',filename=result_filename)
    return jsonify({'success':200,"msg":"上传成功","resultImgUrl":resultImgUrl})

@app.route('/uploaded-images')
def show_images():
    return render_template('showImg_ex.html')

@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/test')
def show_pictures():
    return render_template('history.html')


@app.route('/uploads/<path:filename>')
def get_picture(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/history-filename', methods=['GET','POST'])
def history_filename():
    dir = "uploads"
    list_filename = os.listdir(dir)
    session['filenames'] = list_filename
    return redirect(url_for('show_pictures'))

if __name__ == '__main__':
    app.run()
