@app.route('/volunteers')
def volunteers():
    if isSessionSet():
        con = mysql_app.connect()
        id_1 = session['v_id']
        cur = con.cursor()
        cur.execute("BEGIN")
        cur.execute("select * from volunteer WHERE 1=0 FOR UPDATE")
        cur.execute("commit")
        data = cur.fetchall()

        cur.close()
        con.close()
        return render_template('volunteer.html', data=data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))
    



    @app.route('/volunteers')
def volunteers():
    if isSessionSet():
        con = mysql_app.connect()
        cur = con.cursor()
        cur.execute("select * from volunteer")
        data = cur.fetchall()

        cur.close()
        con.close()
        return render_template('volunteer.html', data=data, path=app.config['UPLOAD_FOLDER'])
    else:
        return redirect(url_for('home'))