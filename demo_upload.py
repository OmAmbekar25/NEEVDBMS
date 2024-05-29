
from fileinput import filename
from flask import Flask, render_template, request, redirect, url_for,session,send_from_directory
from flask_uploads import UploadSet,IMAGES,configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms import SubmitField

app=Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST']='uploads'
app.secret_key="himanipriyaomdhrudiya"

photos=UploadSet('photos',IMAGES)
configure_uploads(app,photos)


class UploadForm(FlaskForm):
    photo=FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File should not empty')
        ]
    )
    submit=SubmitField('Upload')


@app.route('/uploads/<filename>')
def get_files(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)

@app.route('/',methods=['POST','GET'])
def upload_images():
    form=UploadForm()
    if form.validate_on_submit():
        filename=photos.save(form.photo.data)


    return render_template('demo.html',form=form,file_url=url_for('get_file',filename=filename))

if __name__ == '__main__':
    app.run(debug=True)