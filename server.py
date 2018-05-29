from flask import Flask, request, send_from_directory, jsonify

from os import listdir, makedirs
from os.path import isfile, join, exists
from random import shuffle
import shutil

app = Flask(__name__, static_url_path='')

class_dict = {
                0:'bus',
                1:'car',
                2:'moto',
                3:'truck',
                4:'other'
             }

folder_dict = {}

for i in class_dict:
    folder_dict[class_dict[i]] = join('./classified_images', class_dict[i])

for i in class_dict:
    print('%s\t%s' % (i, class_dict[i]))

options = """<div style="width:300px;margin-left: auto;margin-right: auto;"><select size="%s" name="selectionField" style="margin-left: auto;margin-right: auto;font-size:50px;">""" % (len(class_dict) + 1)
options = options + '<option value="-" selected="selected">-</option>'

for i in class_dict:
    #options = options + '<input type="radio" name="id_class" value="%s">%s<br>' % (class_dict[i], class_dict[i])
    options = options + '<option value="%s" >%s</option>' % (class_dict[i], class_dict[i])

options = options + """</select><input id = "submit" type="submit" value="Submit"/></div>"""

print(options)

page = """<!DOCTYPE html>
    <html>
        <head>
            <title>Tagger</title>
            <script src="js/jquery.min.js"></script>
            <script src="js/main.js"></script>
        </head>
        <body>
            <div style="width=100%%">
                <div style="height:300px;width:300px;margin-left: auto;margin-right: auto;">
                    <div id="image_name">%s</div><img id="unclassified_image" src="%s">
                </div>
                """ + options + """
            </div>
        </body>
    </html>"""

images_path = './images/'

@app.route('/images/<path:path>')
def send_img(path):
    return send_from_directory('images', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/tagger')
def tagger():
    onlyfiles = [f for f in listdir(images_path) if isfile(join(images_path, f))]
    if len(onlyfiles) > 0:
        shuffle(onlyfiles)
        file_name = onlyfiles[0]
        return page % (file_name, ('http://127.0.0.1:8080/images/%s' % file_name))
    else:
        return "No more images"

@app.route('/random_image')
def random_image():
    onlyfiles = [f for f in listdir(images_path) if isfile(join(images_path, f))]
    if len(onlyfiles) > 0:
        shuffle(onlyfiles)
        file_name = onlyfiles[0]
        return jsonify({'image_name': file_name})
    else:
        return "No more images"

@app.route('/image_statistics')
def image_statistics():
    ret_dict = {}
    classified_images = 0
    no_cars = 0
    for i in folder_dict:
        onlyfiles = [f for f in listdir(folder_dict[i]) if isfile(join(folder_dict[i], f))]
        print(folder_dict[i])
        if i != 'car':
            no_cars = no_cars + len(onlyfiles)
        classified_images = classified_images + len(onlyfiles)
        ret_dict[i] = len(onlyfiles)
    onlyfiles = [f for f in listdir(images_path) if isfile(join(images_path, f))]
    ret_dict['unclassified'] = len(onlyfiles)
    ret_dict['total'] = classified_images
    ret_dict['no_cars'] = no_cars
    return jsonify(ret_dict)

@app.route('/move/<image_name>/<class_id>', methods=['GET'])
def move(image_name,class_id):
    if class_id != '-':
        for d in folder_dict:
            if not exists(folder_dict[d]):
                makedirs(folder_dict[d])
        image_path = join(images_path, image_name)
        print(image_path)
        shutil.move(image_path, join(folder_dict[class_id], image_name))
    return 'OK'

#http://127.0.0.1:8080/images/im_41000_406_6806.png

if __name__ == "__main__":
    app.run(port=8080)