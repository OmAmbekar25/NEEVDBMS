
from distutils.log import error
from fileinput import filename
from importlib.resources import path
import os
from flask import Flask, render_template, request, redirect, url_for, session
import config
from flaskext.mysql import MySQL
from datetime import date
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import random
import requests
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = "himanipriyaomdhrudiya"

app.config['MYSQL_DATABASE_HOST'] = config.MYSQL_HOST
app.config['MYSQL_DATABASE_USER'] = config.MYSQL_USER
app.config['MYSQL_DATABASE_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DATABASE_DB'] = config.MYSQL_DB
app.config["MYSQL_DATABASE_PORT"] = 3306
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['UPLOADS_DEFAULT_DEST'] = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


mysql_app = MySQL(app)
oauth = OAuth(app)


session_Set = 0

images = UploadSet('images', IMAGES)
configure_uploads(app, images)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def isSessionSet():
    if session.get('set') == 1:
        return True
    else:
        return False


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.route('/home')
@app.route('/')
def home():
    if isSessionSet():
        return redirect(url_for('dashboard'))
    else:
        return render_template('home.html')


@app.route('/events')
def events():
    return render_template('events.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('member_type', None)
    session.pop('email', None)
    session.pop('password', None)
    session.pop('set', 0)

    return redirect(url_for('login'))


@app.route('/login_auth', methods=['POST'])
def login_auth():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from admin where Email=%s and Password=%s",
                    (request.form['email'], request.form['password']))
        data_admin = cur.fetchall()

        cur.execute("select * from neev_members where Email=%s and Password=%s",
                    (request.form['email'], request.form['password']))
        data_member = cur.fetchall()

        cur.close()
        con.close()

        if len(data_member) == 0 and len(data_admin) == 0:
            return render_template('login.html', error=1)
        elif len(data_admin) == 1:
            session['member_type'] = 'admin'
        else:
            session['member_type'] = 'member'

        global session_Set
        session_Set = 1
        session['set'] = 1
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        # 1=> member and 2=>admin
        return redirect(url_for('dashboard', session=session))
    else:
        return render_template('home.html')


@app.route("/signin_google")
def googleCallback():
    # fetch access token and id token using authorization code
    token = oauth.neev.authorize_access_token()

    # google people API - https://developers.google.com/people/api/rest/v1/people/get
    # Google OAuth 2.0 playground - https://developers.google.com/oauthplayground
    # make sure you enable the Google People API in the Google Developers console under "Enabled APIs & services" section

    # # fetch user data with access token
    # personDataUrl = "https://people.googleapis.com/v1/people/me?personFields=genders,birthdays"
    # personData = requests.get(personDataUrl, headers={
    #     "Authorization": f"Bearer {token['access_token']}"
    # }).json()
    # token["personData"] = personData
    # set complete user information in the session
    session["user"] = token
    return redirect(url_for('demo'))


@app.route("/google_login")
def googleLogin():
    if "user" in session:
        # abort(404)
        return redirect(url_for('home'))

    appConf = {
        "OAUTH2_CLIENT_ID": '623228185023-897tsq6uvosj3p7pco37l630p7bjh7im.apps.googleusercontent.com',
        "OAUTH2_CLIENT_SECRET": "LB9mvfPk4fX2rdVRLo0wHD2vASdp",
        "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
        "FLASK_PORT": 5000
    }

    oauth.register(
        "neev",
        client_id=appConf.get("OAUTH2_CLIENT_ID"),
        client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
    )
    return oauth.neev.authorize_redirect(redirect_uri=url_for("googleCallback"))


@app.route('/dashboard')
def dashboard():
    if isSessionSet():
        return render_template('dashboard.html', session=session)
    else:
        return redirect(url_for('home'))


@app.route('/profile')
def display_profile():
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        if session['member_type'] == 'admin':
            cur.execute("select * from admin where Email=%s and Password=%s",
                        (session['email'], session['password']))
        else:
            cur.execute("select * from neev_members where Email=%s and Password=%s",
                        (session['email'], session['password']))
        data = cur.fetchone()
        cur.close()
        con.close()
    else:
        return redirect(url_for('home'))

    return render_template('profile.html', data=data, path=app.config['UPLOAD_FOLDER'], type=session['member_type'])


@app.route('/volunteers')
def volunteers():
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("BEGIN")
        cur.execute("select * from volunteer where V_ID = %s LOCK IN SHARE MODE" , (id_1,))
        cur.execute("commit")
        data = cur.fetchall()

        cur.close()
        con.close()
        return render_template('volunteer.html', data=data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))


@app.route('/update_volunteer_link/<s_id>')
def update_volunteer_link(s_id):
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from volunteer where v_id=%s", (s_id))
        member_data = cur.fetchall()
        cur.close()
        con.close()
        return render_template('update_volunteer.html', data=member_data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))

# modification


@app.route('/update_volunteer', methods=['POST', 'GET'])
def update_volunteer():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        sql = "UPDATE volunteer SET Name=%s, Email=%s,Identification_ID=%s,Gender=%s,Address=%s,Photo=%s,Phone_No=%s WHERE v_id=%s"

        if request.files['photo'].filename == '':
            sql_2 = "UPDATE volunteer SET Name=%s, Email=%s,Identification_ID=%s,Gender=%s, Address=%s,Phone_No=%s WHERE M_id=%s"

            cur.execute(sql_2, (request.form['name'], request.form['email'],
                                request.form['adhar_id'], request.form['gender'], request.form['designation'],
                                request.form['phone'], request.form['v_id']))
            con.commit()
            app.logger.info("nothing")
        else:
            file = request.files['photo']
            filename = file.filename.rsplit('.', 1)[0].lower() + str(int(random.random() * 4500)) + '.' + \
                file.filename.rsplit('.', 1)[1].lower()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            if file and allowed_file(file.filename):
                file.save(filepath)
            else:
                return render_template('update_member.html', error=2, path=app.config['UPLOAD_FOLDER'])

            cur.execute(sql, (request.form['name'], request.form['email'], request.form['adhar_id'],
                        request.form['gender'], request.form['designation'], filename, request.form['phone'], request.form['v_id']))
            con.commit()
            app.logger.info("else")

        cur.close()
        con.close()
        return redirect(url_for('volunteers'))
    else:
        return redirect(url_for('home'))


@app.route('/delete_volunteer/<s_id>')
def delete_volunteer(s_id):
    if isSessionSet():
        sql = "DELETE FROM volunteer WHERE v_id=%s"

        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute(sql, s_id)
        con.commit()

        cur.close()
        con.close()

        return redirect(url_for('volunteers'))
    else:
        return redirect(url_for('home'))


@app.route('/add_volunteer_link')
def add_volunteer_link():
    if isSessionSet():
        return render_template('add_volunteer.html')
    else:
        return redirect(url_for('home'))


@app.route('/insert_volunteer', methods=['POST', 'GET'])
def insert_volunteer():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        file = request.files['photo']
        filename = file.filename.rsplit('.', 1)[0].lower() + str(int(random.random() * 4500)) + '.' + \
            file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if file and allowed_file(file.filename):
            file.save(filepath)
        else:
            return render_template('add_volunteer.html', error=2)

        cur.execute("SELECT * FROM volunteer WHERE Email=%s",
                    (request.form['email']))
        email_data = cur.fetchall()

        if len(email_data) > 0:
            return render_template('add_volunteer.html', error=3)

        cur.execute("INSERT INTO volunteer (Name, Email, Identification_ID, Gender,\
             Address, Photo,Phone_no) VALUES \
             (%s,%s,%s,%s,%s,%s,%s)",
                    (request.form['name'], request.form['email'], request.form['adhar_id'], request.form['gender'],
                     request.form['designation'], filename, request.form['phone']))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('volunteers'))
    else:
        return redirect(url_for('home'))


@app.route('/students')
def students():
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from students")
        data = cur.fetchall()

        cur.close()
        con.close()
        return render_template('students.html', data=data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))


@app.route('/update_student_link/<s_id>')
def update_student_link(s_id):
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from students where s_id=%s", (s_id))
        member_data = cur.fetchall()
        cur.close()
        con.close()
        return render_template('update_student.html', data=member_data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))

# modification


@app.route('/update_student', methods=['POST', 'GET'])
def update_student():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        sql = "UPDATE students SET Name=%s, \
        Email=%s,Identification_ID=%s,Gender=%s,\
        Family_Background=%s,Photo=%s,Phone_No=%s,Address=%s WHERE s_id=%s"

        if request.files['photo'].filename == '':
            sql_2 = "UPDATE students SET Name=%s, \
        Email=%s,Identification_ID=%s,Gender=%s,\
        Family_Background=%s,Phone_No=%s,Address=%s WHERE s_id=%s"

            cur.execute(sql_2, (request.form['name'], request.form['email'],
                                request.form['adhar_id'], request.form['gender'], request.form['fam_background'],
                                request.form['phone'], request.form['designation'], request.form['s_id']))
            con.commit()
            app.logger.info("nothing")
        else:
            file = request.files['photo']
            filename = file.filename.rsplit('.', 1)[0].lower() + str(int(random.random() * 4500)) + '.' + \
                file.filename.rsplit('.', 1)[1].lower()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            if file and allowed_file(file.filename):
                file.save(filepath)
            else:
                return render_template('update_student.html', error=2, path=app.config['UPLOAD_FOLDER'])

            cur.execute(sql, (request.form['name'], request.form['email'], request.form['adhar_id'],
                              request.form['gender'], request.form['fam_background'], filename, request.form['phone'], request.form['designation'],
                              request.form['s_id']))
            con.commit()
            app.logger.info("else")

        cur.close()
        con.close()
        return redirect(url_for('students'))
    else:
        return redirect(url_for('home'))


@app.route('/delete_student/<s_id>')
def delete_student(s_id):
    if isSessionSet():
        sql = "DELETE FROM students WHERE s_id=%s"

        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute(sql, s_id)
        con.commit()

        cur.close()
        con.close()

        return redirect(url_for('students'))
    else:
        return redirect(url_for('home'))


@app.route('/add_student_link')
def add_student_link():
    if isSessionSet():
        return render_template('add_student.html')
    else:
        return redirect(url_for('home'))


@app.route('/insert_student', methods=['POST', 'GET'])
def insert_student():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        file = request.files['photo']
        filename = file.filename.rsplit('.', 1)[0].lower() + str(int(random.random() * 4500)) + '.' + \
            file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if file and allowed_file(file.filename):
            file.save(filepath)
        else:
            return render_template('add_student.html', error=2)

        cur.execute("SELECT * FROM students WHERE Email=%s",
                    (request.form['email']))
        email_data = cur.fetchone()

        if email_data != None:
            return render_template('add_student.html', error=3)

        cur.execute("INSERT INTO students (Name, Email, Identification_ID, Gender,\
             Address, Photo, Phone_No,Family_Background) VALUES \
             (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (request.form['name'], request.form['email'], request.form['Identification_id'], request.form['gender'],
                     request.form['Address'], filename, request.form['phone'], request.form['fam_background']))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('students'))
    else:
        return redirect(url_for('home'))


@app.route('/instructors')
def instructors():
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from instructors")
        data = cur.fetchall()

        cur.close()
        con.close()
        return render_template('instructor.html', data=data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))


@app.route('/update_instructor_link/<s_id>')
def update_instructor_link(s_id):
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from instructors where i_id=%s", (s_id))
        member_data = cur.fetchall()
        cur.close()
        con.close()
        return render_template('update_instructor.html', data=member_data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))

# modification


@app.route('/update_instructor', methods=['POST', 'GET'])
def update_instructor():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        sql = "UPDATE instructors SET Name=%s, \
        Email=%s,Identification_ID=%s,Gender=%s,\
        Phone_No=%s,Type=%s WHERE i_id=%s"

        cur.execute(sql, (request.form['name'], request.form['email'],
                          request.form['adhar_id'], request.form['gender'],
                          request.form['phone'], request.form['Type'], request.form['i_id']))
        con.commit()
        app.logger.info("else")

        cur.close()
        con.close()
        return redirect(url_for('instructors'))
    else:
        return redirect(url_for('home'))


@app.route('/delete_instructor/<s_id>')
def delete_instructor(s_id):
    if isSessionSet():
        sql = "DELETE FROM instructors WHERE i_id=%s"

        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute(sql, s_id)
        con.commit()

        cur.close()
        con.close()

        return redirect(url_for('instructors'))
    else:
        return redirect(url_for('home'))


@app.route('/add_instructor_link')
def add_instructor_link():
    if isSessionSet():
        return render_template('add_instructor.html')
    else:
        return redirect(url_for('home'))


# @app.route('/add_student_inst_link')
# def add_student_inst_link():
#     if isSessionSet():
#         return render_template('add_student_instructor.html')
#     else:
#         return redirect(url_for('home'))

@app.route('/insert_instructor', methods=['POST', 'GET'])
def insert_instructor():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        # file = request.files['photo']
        # filename= file.filename.rsplit('.', 1)[0].lower() + str(int(random.random() * 4500)) + '.' + \
        # file.filename.rsplit('.', 1)[1].lower()
        # filepath=os.path.join(app.config['UPLOAD_FOLDER'],filename)

        # if file and allowed_file(file.filename):
        #     file.save(filepath)
        # else:
        #     return render_template('add_instructor.html',error=2)

        cur.execute("SELECT * FROM instructors WHERE Email=%s",
                    (request.form['email']))
        email_data = cur.fetchone()

        if email_data != None:
            return render_template('add_instructor.html', error=3)

        cur.execute("INSERT INTO instructors (Name, Email, Identification_ID, Gender,\
            Type, Phone_No) VALUES \
             (%s,%s,%s,%s,%s,%s)",
                    (request.form['name'], request.form['email'], request.form['Identification_id'], request.form['gender'],
                     request.form['Type'], request.form['phone']))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('instructors'))
    else:
        return redirect(url_for('home'))


@app.route('/donors')
def donors():
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from donation")
        data = cur.fetchall()

        cur.close()
        con.close()
        return render_template('donor.html', data=data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))


@app.route('/update_donor_link/<m_id>')
def update_donor_link(m_id):
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from donation where d_id=%s", (m_id))
        donor_data = cur.fetchall()
        cur.close()
        con.close()
        return render_template('update_donor.html', data=donor_data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))


@app.route('/update_donor', methods=['POST', 'GET'])
def update_donor():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        sql = "UPDATE donation SET Donor_Name=%s, \
        Email=%s,Amount=%s, Details=%s, \
        Phone_No=%s WHERE d_id=%s"

        cur.execute(sql, (request.form['name'],
                          request.form['email'], request.form['Amount'], request.form['Details'],
                          request.form['phone'], request.form['m_id']))
        con.commit()
        app.logger.info("else")

        cur.close()
        con.close()
        return redirect(url_for('donors'))
    else:
        return redirect(url_for('home'))


@app.route('/add_donor')
def add_donor():
    if isSessionSet():
        return render_template('add_donor.html')
    else:
        return redirect(url_for('home'))


@app.route('/insert_donor', methods=['POST', 'GET'])
def insert_donor():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        cur.execute("SELECT * FROM donation WHERE Email=%s",
                    (request.form['email']))
        email_data = cur.fetchone()

        if email_data != None:
            return render_template('add_donor.html', error=3)

        cur.execute("INSERT INTO donation (Donor_Name, Email, Amount, Details,Phone_No) VALUES \
             (%s,%s,%s,%s,%s)",
                    (request.form['name'], request.form['email'], request.form['Amount'], request.form['Details'],
                     request.form['phone']))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('donors'))
    else:
        return redirect(url_for('home'))


@app.route('/members')
def members():
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from neev_members")
        data = cur.fetchall()

        cur.close()
        con.close()
        return render_template('member.html', data=data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))


@app.route('/update_member_link/<m_id>')
def update_member_link(m_id):
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from neev_members where M_id=%s", (m_id))
        member_data = cur.fetchall()
        cur.close()
        con.close()
        return render_template('update_member.html', data=member_data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))


@app.route('/update_member', methods=['POST', 'GET'])
def update_member():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        sql = "UPDATE neev_members SET Name=%s, \
        Email=%s,Identification_ID=%s,Gender=%s,\
        Designation=%s,Photo=%s,Phone_No=%s WHERE M_id=%s"

        if request.files['photo'].filename == '':
            sql_2 = "UPDATE neev_members SET Name=%s, \
            Email=%s,Identification_ID=%s,Gender=%s,\
            Designation=%s,Phone_No=%s WHERE M_id=%s"

            cur.execute(sql_2, (request.form['name'], request.form['email'], request.form['adhar_id'],
                                request.form['gender'], request.form['designation'], request.form['phone'], request.form['m_id']))
            con.commit()
            app.logger.info("nothing")
        else:
            file = request.files['photo']
            filename = file.filename.rsplit('.', 1)[0].lower() + str(int(random.random() * 4500)) + '.' + \
                file.filename.rsplit('.', 1)[1].lower()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            if file and allowed_file(file.filename):
                file.save(filepath)
            else:
                return render_template('update_member.html', error=2, path=app.config['UPLOAD_FOLDER'])

            cur.execute(sql, (request.form['name'], request.form['email'], request.form['adhar_id'],
                        request.form['gender'], request.form['designation'], filename, request.form['phone'], request.form['m_id']))
            con.commit()
            app.logger.info("else")

        cur.close()
        con.close()
        return redirect(url_for('members'))
    else:
        return redirect(url_for('home'))


@app.route('/delete_member/<m_id>')
def delete_member(m_id):
    if isSessionSet():
        sql = "DELETE FROM neev_members WHERE M_id=%s"

        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute(sql, m_id)
        con.commit()

        cur.close()
        con.close()

        return redirect(url_for('members'))
    else:
        return redirect(url_for('home'))


@app.route('/add_member')
def add_member():
    if isSessionSet():
        return render_template('add_member.html')
    else:
        return redirect(url_for('home'))


@app.route('/insert_member', methods=['POST', 'GET'])
def insert_member():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        file = request.files['photo']
        filename = file.filename.rsplit('.', 1)[0].lower() + str(int(random.random() * 4500)) + '.' + \
            file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if file and allowed_file(file.filename):
            file.save(filepath)
        else:
            return render_template('add_member.html', error=2)

        cur.execute("SELECT * FROM neev_members WHERE Email=%s",
                    (request.form['email']))
        email_data = cur.fetchone()

        if email_data != None:
            return render_template('add_member.html', error=3)

        # error 3 -> email already exist
        # error 2 -> file not allowed

        cur.execute("INSERT INTO neev_members(Name, Email, Identification_ID, Gender,\
             Designation, Photo, Password, Phone_No) VALUES \
             (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (request.form['name'], request.form['email'], request.form['adhar_id'], request.form['gender'],
                     request.form['designation'], filename, request.form['password'], request.form['phone']))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('members'))
    else:
        return redirect(url_for('home'))


@app.route('/courses')
def courses():
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from course")
        data = cur.fetchall()

        cur.close()
        con.close()
        return render_template('courses.html', data=data)
    else:
        return redirect(url_for('home'))

# tuple(item for subtuple in active_courses for item in subtuple)


@app.route('/activate_course/<id>')
def activate_course(id):
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from course where C_ID=%s", id)
        data = cur.fetchall()

        cur.execute("select * from instructors")
        instructors = cur.fetchall()

        cur.close()
        con.close()
        current_date = date.today().isoformat()

        return render_template('activate_course.html', data=data[0], ins=instructors, date=current_date)
    else:
        return redirect(url_for('home'))


@app.route('/activate_course/done_activate', methods=['POST'])
def done_activate():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        cur.execute("INSERT INTO active_courses (I_ID, C_ID, start_date, end_date) VALUES (%s,%s,%s,%s)",
                    (request.form['instructor'], request.form['courseId'], request.form['startDate'], request.form['endDate'],))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('courses'))
    else:
        return redirect(url_for('home'))


@app.route('/update/<id>')
def update_link(id):
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from course where C_ID=%s", (id))
        course_data = cur.fetchall()
        cur.close()
        con.close()
        return render_template('update_course.html', data=course_data)
    else:
        return redirect(url_for('home'))


@app.route('/update_course', methods=['POST'])
def update_course():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        cur.execute("UPDATE  course SET Course_name =%s, Details =%s, Venue =%s WHERE C_ID=%s",
                    (request.form['name'], request.form['Details'], request.form['Venue'], request.form['id']))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('courses'))
    else:
        return redirect(url_for('home'))


@app.route('/course_details/<id>')
def course_details(id):
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from course where C_ID=%s", (id))
        course_data = cur.fetchall()

        cur.execute(
            "select name from active_courses natural join instructors where C_ID=%s", (id))
        inst = cur.fetchall()
        inst = tuple(item for subtuple in inst for item in subtuple)

        cur.execute("select * from active_courses where C_ID=%s", (id))
        active_part = cur.fetchall()

        stu = []
        stu_len = []
        vol = []
        vol_len = []
        all_stu = []
        all_vol = []
        for i in active_part:
            cur.execute(
                "select s_id,name,email  from students where s_id in (select s_id from active_courses NATURAL join student_course where active_id=%s)", (i[4]))
            rel = cur.fetchall()
            stu.append(rel)
            stu_len.append(len(rel))

            cur.execute(
                "select v_id,name  from volunteer where v_id in ( select v_id  from active_courses NATURAL join volunteer_course where active_id=%s)", (i[4]))
            rel_vol = cur.fetchall()
            vol.append(rel_vol)
            vol_len.append(len(rel_vol))

            cur.execute(
                "select S_ID,name from students where S_ID NOT IN (select S_ID from active_courses NATURAL join student_course where active_id=%s)", (i[4]))
            all_stu.append(cur.fetchall())

            cur.execute(
                "select v_id,name,email from volunteer where v_id not in ( select v_id  from active_courses NATURAL join volunteer_course where active_id=%s)", (i[4]))
            all_vol.append(cur.fetchall())

        cur.close()
        con.close()

        return render_template('course_details.html', course=course_data, instructors=inst, stud_not_in_course=all_stu,
                               vol_not_in_course=all_vol, active_course=active_part, students=stu, stu_count=stu_len, volunteers=vol, vol_count=vol_len)
    else:
        return redirect(url_for('home'))


@app.route('/en_stu', methods=['POST'])
def en_stu():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        cur.execute("INSERT INTO student_course (S_ID, active_id) VALUES (%s,%s)",
                    (request.form['student_enr'], request.form['active_course_id']))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('course_details', id=request.form['course_id']))
    else:
        return redirect(url_for('home'))


@app.route('/en_vol', methods=['POST'])
def en_vol():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        cur.execute("INSERT INTO volunteer_course (V_ID, active_id) VALUES (%s,%s)",
                    (request.form['vol_en'], request.form['active_course_id']))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('course_details', id=request.form['course_id']))
    else:
        return redirect(url_for('home'))

# for adding new course


@app.route('/add_course')
def add_course():
    return render_template('add_course.html')


@app.route('/add_course_detail', methods=['POST', 'GET'])
def add_course_detail():
    if request.method == 'POST':
        con = mysql_app.connect()
        cur = con.cursor()

        cur.execute("insert into course (C_ID,Course_name,Details,Venue) values (%s,%s,%s,%s)",
                    (request.form['id'], request.form['name'], request.form['Details'], request.form['Venue'],))
        con.commit()

        cur.close()
        con.close()
        return redirect(url_for('courses'))
    else:
        return redirect(url_for('home'))


@app.route('/demo')
def demo():
    return render_template('demo.html')


if __name__ == '__main__':
    app.run(debug=False,host='127.0.0.1',port=5000)
