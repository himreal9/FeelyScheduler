from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, flash, session
from datetime import datetime


app=Flask(__name__)
app.secret_key='man'
app.config['MYSQL_USER'] = 'sql6457643'
app.config['MYSQL_PASSWORD'] = 'ZLkEwHLtMd'
app.config['MYSQL_DB'] = 'sql6457643'
app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)

@app.route('/') 
def con():
    session.pop('user',None)
    session.pop('euser',None)
    return render_template('main.html')

@app.route('/man', methods=['GET', 'POST'])
def con1():
    if 'user' in session:
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM time WHERE dt < CURDATE()")
        mysql.connection.commit()
        cur.execute("select * from time order by dt desc")
        mysql.connection.commit()
        r=cur.fetchall()
        h=['Date','Slot Time','Status']
        l1=[]
        k=[]
        cur.execute("select CURDATE()")
        mysql.connection.commit()
        d=cur.fetchall()
        for i in d:
            d=i['CURDATE()']
        for i in r:
            l=[i["date"],i["time"],i["status"]]
            k.append(i["date"]+' '+i["time"])
            l1.append(l)
        if request.method=='POST':
            if request.form.get("ln"):
                hr = request.form['hr']
                mi = request.form['min']
                am = request.form['am']
                date = request.form['da']
                time = hr+":"+mi+" "+am
                dt=date+' '+time
                dt=datetime.strptime(dt, '%Y-%m-%d %H:%M %p').isoformat()
                if dt not in k:
                    cur.execute("insert into time values (%s,%s,%s,'open')",(dt,date,time))
                    mysql.connection.commit()
                    flash('Added Successfully')
                    return redirect('/man')
                else:
                    flash('Already Scheduled')
                    return redirect('/man')
        return render_template('manmain.html',h=h,l1=l1,d=d)
    else:
        return redirect('/')
        
@app.route('/emp', methods=['GET', 'POST'])
def con2():
    if 'euser' in session:
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM time WHERE dt < CURDATE()")
        mysql.connection.commit()
        cur.execute("select * from time where status like '%open%' order by dt desc")
        mysql.connection.commit()
        r=cur.fetchall()
        h=[]
        h1=[]
        h2=[]
        cur.execute("select CURDATE()")
        mysql.connection.commit()
        d=cur.fetchall()
        for i in d:
            d=i['CURDATE()']
        for i in r:
            h.append(i["date"]+' '+i["time"])
        p=session['euser']
        cur.execute(f"SELECT * FROM time WHERE status NOT LIKE '%open%' and status like '%{p}%' order by dt desc")
        mysql.connection.commit()
        r=cur.fetchall()
        for i in r:
            h1.append(i["date"]+' '+i["time"]+" (Booked By You)")
        cur.execute(f"SELECT * FROM time WHERE status NOT LIKE '%open%' and status not like '%{p}%' order by dt desc")
        mysql.connection.commit()
        r=cur.fetchall()
        for i in r:
            h2.append(i["date"]+' '+i["time"])
        if request.method=='POST':
            k = request.form.getlist('list')
            for i in k:
                dt=datetime.strptime(i, '%Y-%m-%d %H:%M %p').isoformat()
                dt=str(dt).replace('T',' ')
                cur.execute("update time set status=%s where dt like %s",('Meeting with'+session['euser'],dt))
                mysql.connection.commit()
            return redirect('/emp')
        return render_template('empmain.html',h=h,d=d,h1=h1,h2=h2)
    else:
        return redirect('/')
    
@app.route('/emplog', methods=['GET', 'POST'])
def emplogin():
    if request.method=='POST':
        if request.form.get("ln"):
            unam = request.form['unam']
            pas = request.form['pas']
            cur=mysql.connection.cursor()
            cur.execute("select * from emp where user like %s",(unam,))
            mysql.connection.commit()
            r=cur.fetchall()
            if len(r)!=0:               
                if unam==r[0]['user'] and pas==r[0]['pass']:
                    session['euser']=unam
                    return redirect("/emp")
                else:
                    flash("Wrong credentials")
                    return redirect('/emplog')
            else:
                flash("Wrong credentials")
                return redirect('/emplog')
    else:
        return render_template('login.html')
    
@app.route('/manlog', methods=['GET', 'POST'])
def manlogin():
    if request.method=='POST':
        if request.form.get("ln"):
            unam = request.form['unam']
            pas = request.form['pas']
            cur=mysql.connection.cursor()
            cur.execute("select * from man where user like %s",(unam,))
            mysql.connection.commit()
            r=cur.fetchall()
            if len(r)!=0:               
                if unam==r[0]['user'] and pas==r[0]['pass']:
                    session['user']=unam
                    return redirect("/man")
                else:
                    flash("Wrong credentials")
                    return redirect("/manlog")
            else:
                flash("Wrong credentials")
                return redirect("/manlog")
    else:
        return render_template('login1.html')
    
if __name__=='__main__':
    app.run()
