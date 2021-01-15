import json
import os
import uuid

from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session, jsonify
from flask_dropzone import Dropzone
from caller import userTest

from imageHandle import imageHandle

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

#主页面
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')

#随机图片名字
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

#接受前端的图片，并返回服务器保存的图片路径用于显示
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if len(str(request.files.get('photo').filename)) != 0:
        img = request.files.get('photo')
        filename = random_filename(img.filename)
        img.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        img_url = "uploads/"+filename
        return jsonify({'success':200,"msg":"上传成功","img_url":img_url})
    else:
        return jsonify({'success':404,"msg":"上传失败","img_url":""})

#获得结果图片路径
@app.route('/renet50/results_user_test/<path:filename>')
def get_result(filename):
    return send_from_directory(app.config['RESULT_PATH'], filename)

#预测图片
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
    #测试用
    #resultImgUrl = ""
    #itemsNum = str([{"name":"道路","num":1},{"name":"行人","num":2},{"name":"红绿灯","num":1}])
    #itemsArea = str([{"name":"道路","area":120},{"name":"行人","area":50},{"name":"红绿灯","area":80}])

    resultHandle = imageHandle(os.path.join(app.config['RESULT_PATH'], result_filename))
    #测试用
    #resultHandle = [('vegetation', 49.31), ('road', 27.36), ('building', 15.24), ('fence', 2.0), ('sidewalk', 1.87), ('sky', 1.74), ('person', 0.79), ('terrain', 0.64), ('car', 0.37), ('traffic sign', 0.28), ('pole', 0.25), ('wall', 0.15), ('bus', 0.0)]

    #将数据转换为JSON格式，并且最大的5个之后归类为其他
    #这两个分别用于表格和饼图展示
    itemsNum = list()
    itemsArea = list()
    for result in resultHandle[:5]:
        itemsNum.append({'name':result[0],'num':result[1]})
        itemsArea.append({'name':result[0],'area':result[1]})
    for i in range(5,len(resultHandle)):
        if i==5:
            itemsNum.append({'name': 'others', 'num': resultHandle[i][1]})
            itemsArea.append({'name': 'others', 'area': resultHandle[i][1]})
        else:
            itemsNum[5]['num']+=resultHandle[i][1]
            itemsArea[5]['area']+=resultHandle[i][1]
        if i == len(resultHandle)-1:
            itemsNum[5]['num'] = round(itemsNum[5]['num'],2)
            itemsArea[5]['area'] = round(itemsArea[5]['area'], 2)
    itemsNum = str(itemsNum)
    itemsArea = str(itemsArea)
    return jsonify({'success':200,"msg":"上传成功","resultImgUrl":resultImgUrl,"itemsNum":itemsNum,"itemsArea":itemsArea})

#跳转至历史记录页面
@app.route('/test')
def show_pictures():
    return render_template('history.html')

#用于历史记录页面获得文件夹的图片
@app.route('/uploads/<path:filename>')
def get_picture(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

#相应查看历史记录图片按钮
@app.route('/history-filename', methods=['GET','POST'])
def history_filename():
    dir = "uploads"
    list_filename = os.listdir(dir)
    session['filenames'] = list_filename
    return redirect(url_for('show_pictures'))

if __name__ == '__main__':
    app.run()
