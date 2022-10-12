from flask import Flask, render_template, request, session,  redirect, url_for;
from werkzeug.utils import secure_filename;
import ibm_db;
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wcp83609;PWD=los9tJgWglPoScvy",'','')

app= Flask(__name__)
app.secret_key="SecretKey";

@app.route("/")
def home():
    return render_template("home.html");

@app.route("/addstudent")
def new_student():
    return render_template("add_student.html");

@app.route("/addrec", methods=['GET','POST'])
def addrec():
    if request.method == 'POST':
    
            name=request.form['name'];
            addr=request.form['address'];
            city=request.form['city'];
            pin=request.form['pin'];

            sql="SELECT * FROM students WHERE name=?"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,name)
            ibm_db.execute(stmt)
            account=ibm_db.fetch_assoc(stmt)
            print(account)
            #return "Success..."+name

            if account:
                return render_template("list.html",msg="You are already a member")
            else:
                insert_sql="INSERT INTO students VALUES(?,?,?,?)"
                prep_stmt=ibm_db.prepare(conn,insert_sql)
                ibm_db.bind_param(prep_stmt,1,name)    
                ibm_db.bind_param(prep_stmt,2,addr)    
                ibm_db.bind_param(prep_stmt,3,city)    
                ibm_db.bind_param(prep_stmt,4,pin)
                ibm_db.execute(prep_stmt)    
                return render_template("list.html",msg="Student data saved successfully")
        
            


@app.route('/list')
def list():
  students = []
  sql = "SELECT * FROM Students"
  stmt = ibm_db.exec_immediate(conn, sql)
  dictionary = ibm_db.fetch_both(stmt)
  while dictionary != False:
    # print ("The Name is : ",  dictionary)
    students.append(dictionary)
    dictionary = ibm_db.fetch_both(stmt)

  if students:
    return render_template("list.html", students = students)