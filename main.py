from flask import Flask, render_template, Response, request, redirect
from camera import VideoCamera
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "./videos"

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)
            else:
                    
                filename = secure_filename(image.filename)

                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                
                return redirect(request.url)
            
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
