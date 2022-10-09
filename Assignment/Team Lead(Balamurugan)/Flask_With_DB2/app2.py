from flask import Flask, render_template, request, session,escape,  redirect, url_for
from werkzeug.utils import secure_filename;
import ibm_db;
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bkj82229;PWD=KCwhio0Cb0XQmB5H",'','')

app = Flask(__name__)
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


@app.route('/delete/<name>')
def delete(name):
  sql = f"SELECT * FROM Students WHERE name='{escape(name)}'"
  print(sql)
  stmt = ibm_db.exec_immediate(conn, sql)
  student = ibm_db.fetch_row(stmt)
  print ("The Name is : ",  student)
  if student:
    sql = f"DELETE FROM Students WHERE name='{escape(name)}'"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)

    students = []
    sql = "SELECT * FROM Students"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
      students.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
    if students:
      return render_template("list.html", students = students, msg="Delete successfully")


  
  # # while student != False:
  # #   print ("The Name is : ",  student)

  # print(student)
  return "success..."

# @app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
# def edit(id):
    
#     post = BlogPost.query.get_or_404(id)

#     if request.method == 'POST':
#         post.title = request.form['title']
#         post.author = request.form['author']
#         post.content = request.form['content']
#         db.session.commit()
#         return redirect('/posts')
#     else:
#         return render_template('edit.html', post=post)