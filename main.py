from flask import Flask, render_template, request, flash
import os
import cv2
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and file name is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            Newfilename= f"static/{filename}"
            cv2.imwrite(Newfilename, imgProcessed)
            return Newfilename
        
        case "cwebp":
            Newfilename= f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(Newfilename, img)
            return Newfilename
        
        case "cjpg":
            Newfilename= f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(Newfilename, img)
            return Newfilename
        
        case "cpng":
            Newfilename= f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(Newfilename, img)
            return Newfilename


    pass

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == 'POST':
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"your image has been processed and is available <a href='/{new}'target='_blank'>here</a>")

            # processImage()
            return render_template("index.html")
        

    return render_template("index.html")


app.run(debug=True, port=5000)