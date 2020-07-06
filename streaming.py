# live_streaming.py

from flask import Flask, render_template, Response
import color_detection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(fr):
    fr.make_background()
    while True:
        jpg_bytes = fr.get_jpg_bytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(color_detection.ColorDetect()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
