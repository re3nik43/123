from flask import Flask, session, redirect, request, url_for, render_template
from main_db_controll import db
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def index():
   return render_template('main.html')
   # if request.method == "POST":
   #    info = request.form.to_dict(flat=False)
   #    db.add_data(info)
   #    data = db.get_data()
   #    return render_template('answer.html', obj=data)

def answer():
   file = request.files['file']
   if file and allowed_file(file.filename):
      # Сохранение файла в указанной папке
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
   form_data = tuple(request.form.values()) + (file.filename,)
   print(form_data)
   db.add_data(form_data)
   data = db.get_data()
   print(data)
   return render_template('answer.html', obj=data)

app = Flask(__name__)
app.add_url_rule('/', 'index', index, methods=["GET"])
app.add_url_rule('/answer', 'answer', answer, methods=["POST"])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if __name__ == '__main__':
   if not os.path.exists(UPLOAD_FOLDER):
      os.makedirs(UPLOAD_FOLDER)
   app.run(debug=True)