import urllib

from flask import request, Flask, make_response, send_from_directory
import os
import time
from reportlab import platypus
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
import uuid
from flask import Flask, request
from PIL import Image
# pip install Pillow
import urllib.request
import platform

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'img2pdf service.'


def getUploadDir():
    if (platform.system() == 'Windows'):
        uploadDir = 'D:\jx\py\img2pdf\img'
    else:
        uploadDir = '/home/fileserver/img'
    return uploadDir;


@app.route('/api/Common/imgToPdf', methods=['GET', 'POST'])
def imgToPdf():
    '''
    http://127.0.0.1:5000/api/Common/imgToPdf?imgurl=https://zyai.jxwifi.com/uploads/20201203/ae26751e48348f0765322f9eb26a5a32.png
    :return:
    '''
    imgurl = request.args.get('imgurl', '')
    x=request.args.get('x',0)
    y=request.args.get('y',0)
    if x=='':
        x=0
    if y=='':
        y=0
    x=int(x)
    y=int(y)
    print('x='+str(x))
    print('y='+str(y))
    filename = topdf(imgurl,x,y)
    return send_from_directory(directory=getUploadDir(),
                               filename=filename,
                               mimetype='application/pdf')


@app.route('/uploadFile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['img']
        f.save(getUploadDir() + '/' + str(uuid.uuid4()) + '.img')


def download_img(img_url, uuidName):
    request = urllib.request.Request(img_url)
    response = urllib.request.urlopen(request)
    imgName = uuidName + "_org.png"
    orgFileName = getUploadDir() + "/" + imgName
    if (response.getcode() == 200):
        with open(orgFileName, "wb") as f:
            f.write(response.read())  # 将内容写入图片
        return imgName
    return None


def topdf(image_file: str,left=0,top=0):
    # image_file: str = "./test.png"
    # image_file = "https://zyai.jxwifi.com/uploads/20201203/ae26751e48348f0765322f9eb26a5a32.png"

    uuidName = str(uuid.uuid4());
    pdfName = uuidName + '.pdf'
    c = canvas.Canvas(getUploadDir() + '/' + pdfName, pagesize=A3)
    width, height = A3

    if image_file[-3:].lower() == 'png':
        jpgName = download_img(image_file, uuidName)
        im = Image.open(getUploadDir() + "/" + jpgName)
        x, y = im.size
        p = Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
        savePath = getUploadDir() + "/" + uuidName + '.png';
        p.save(savePath)
        c.drawImage(savePath, left, top, width, height)
    else:
        #c.drawImage(image_file, 0, 0, width, height)
        #c.drawInlineImage(image_file, 0, 0)
        # c.showPage()
        c.drawImage(image_file, left, top, width, height)
    c.save()
    return pdfName;


if '__main__' == __name__:
    print("开始运行服务")
    app.run('0.0.0.0', 4000, False)
    print("运行服务完成")

