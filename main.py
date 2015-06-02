from flask import Flask, request, abort, send_file
from PIL import Image
import StringIO, urllib2

app = Flask(__name__)

@app.route('/')
def proxy_image():
    if request.args.has_key('url'): img_url = urllib2.unquote(request.args['url'])
    else: abort(400)
    if request.args.has_key('width') and request.args.has_key('height'):
        img_size = int(request.args['width']), int(request.args['height'])
        img_mod = 'direct'
    elif request.args.has_key('width'):
        img_size = int(request.args['width']), 0
        img_mod = 'ratiow'
    elif request.args.has_key('height'):
        img_size = 0, int(request.args['height'])
        img_mod = 'ratioh'
    else: abort(400)
    file_name = str(img_size[0]) + '_' + str(img_size[1]) + '_' + img_mod + '_' + img_url.split('/')[-1]
    file_from_url = False
    try:
        fh = open(file_name)
        print file_name + ' available on disk'
    except:
        fh = urllib2.urlopen(img_url)
        file_from_url = True
        print file_name + ' loaded from url'
    img = Image.open(fh)
    if file_from_url:
        if img_mod == 'direct':
            img = img.resize(img_size, Image.ANTIALIAS)
        elif img_mod == 'ratiow':
            img_size = img_size[0], int(float(img.size[1]) * (float(img_size[0]) / float(img.size[0])))
            img.thumbnail(img_size, Image.BICUBIC)
        elif img_mod == 'ratioh':
            img_size = int(float(img.size[0]) * (float(img_size[1]) / float(img.size[1]))), img_size[1]
            img.thumbnail(img_size, Image.BICUBIC)
        # This save is to store to disk if required to handle files internally
        # img.save(file_name)
    img_io = StringIO.StringIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run()
