from flask import Flask, render_template,request,json,redirect 
from flask_mysqldb import MySQL
import mysql.connector
from sqlalchemy import true 
from flask   import session

app = Flask(__name__)
app.secret_key = 'hello how are you'
conn= mysql.connector.connect(host="localhost",user="root",port="3307",password="",database="checkin")




@app.route("/")
def main():
    return render_template('index.html')
  

@app.route('/signup')
def Showsignup():
    return render_template('signup.html')

@app.route('/api/signup',methods=['POST'])
def signUp():
    try:
        username = request.form['inputName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        selectquery = "select * from accounts where username ='%s' "%username
        cursor=conn.cursor()
        cursor.execute(selectquery)
        data = cursor.fetchall()
        if len(data)== 0:
            conn.commit()
            insertquery="insert into accounts values(null,'%s','%s','%s')"%(username ,password,email )
            cursor.execute(insertquery)
            conn.commit()

            return json.dumps({'message':'User created successfully !'})
            
        else:
            return json.dumps({'error': str(data[0])})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()  


@app.route('/signin')
def showSignin():
    return render_template('signin.html')


@app.route('/api/validateLogin',methods=['POST'])
def validateLogin():
    try:
        email = request.form['inputEmail']
        password = request.form['inputPassword']
 
     # connect to mysql
        print("before proce")
        cursor=conn.cursor()
        cursor.execute("select * from accounts where email ='%s' and password='%s'"%(email,password))
        print('after proc')
        data = cursor.fetchall()
        conn.commit()
        print(data)
        if len(data) > 0:
            session['userid'] = data[0][0]
            print('inside if')
            return  render_template('userhome.html',accounts=data)
            
        else:
            return render_template('error.html',error = 'Wrong Email address or Password')
 
    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/userHome')     
def userHome():
    if session.get('userid'):
        cursor = conn.cursor(buffered=true)
        username =str(session.get('userid'))
        selectquery="select username from accounts where username='%s'"%(username)
        print(selectquery)  
        cursor.execute(selectquery) 
        data= cursor.fetchall() 
        print(data)     
        cursor.close()  
        return render_template('userhome.html',username=data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

# @app.route('/userHome')
# def userhome():
    
#     if session.get('username'):
#         cursor = conn.cursor(buffered=true)
#         username =str(session.get('username'))
#         selectquery="select username from accounts where username='%s'"%(username)
#         print(selectquery)  
#         cursor.execute(selectquery) 
#         data= cursor.fetchall() 
#         print(data)     
#         cursor.close()  
#         return render_template('userhome.html',username=data)   
#     else:
#         return render_template('error.html',error = 'Unauthorized Access')



@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/profile')
def profile():  
    if session.get('userid'):   
        cursor = conn.cursor(buffered=true)
        userid =int(session.get('userid'))
        selectquery="Select * from accounts where id=%d"%(userid)
        print(selectquery)
        cursor.execute(selectquery)
        data= cursor.fetchall()
        print(data)       
        cursor.close()
        return render_template('userprofile.html',userprofile=data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')





@app.route('/Showappointment')       
def Showregister():
    return render_template('appointment.html')

@app.route("/appointment",methods=['GET','POST'])
def registerr():
    if session.get('userid'):
        
        if request.method=='POST': 
            reg=request.form

            fname=str(reg['fname'])
            lname=str(reg['lname'])
            contact=int(reg['contact'])
            aadhar=int(reg['aadhar'])
            gender=str(reg['gender'])
            docn=str(reg['docn'])
            time=str(reg['time'])
            
            cond=str(reg['condition']) 
            # picture=reg['picture']
            user = session.get('userid')
            
            cursor=conn.cursor()
            cursor.execute("insert into register values(null,'%s','%s','%d','%d','%s','%s','%s','%s','%d')" %(fname,lname,contact,aadhar,gender,docn,time,cond,user))
            conn.commit()
            cursor.close()
            return render_template('appointment.html')

        else:
            return render_template('appointment.html')
    
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/Viewappointment')
def viewAppointment():
    if session.get('userid'):
        print("if ke andar")
        # pid = (session.get('pid'))
        userid = int(session.get('userid'))
        cursor = conn.cursor(buffered=true)
        selectquery=("select * from register where user_id = %d")%(userid)
        print(userid)
        cursor.execute(selectquery)
        data= cursor.fetchall()
        print(data) 
        cursor.close()
        return render_template('viewappointment.html',register=data)
    
















# ADMIN PAGE

@app.route('/admin')
def showadmin():
    cursor = conn.cursor(buffered=true)
    selectquery=("SELECT * FROM register ORDER BY register.fname DESC")
    cursor.execute(selectquery)
    data= cursor.fetchall()
    print(data) 
    cursor.close()
    return render_template('admin.html',register=data)
         

@app.route('/facee')
def facee():
    return render_template('face.html') 

print("hi")
if __name__ =='__main__':
    app.run(debug=True)    