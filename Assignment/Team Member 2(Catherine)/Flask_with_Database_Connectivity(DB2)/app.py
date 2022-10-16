from flask import Flask, url_for,render_template,request,config,session,make_response,abort,redirect,flash;
from markupsafe import escape;
import ibm_db;
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wcp83609;PWD=los9tJgWglPoScvy",'','')

app = Flask(__name__);
# app.config['SECRET_KEY'] = 'the secret key'
app.secret_key="SecretKey";

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/signin/")
def signin():
    return render_template("signin.html")

@app.route("/about/")
def about():
    return render_template("about.html")

messages=[{'title':'Message One',
           'content':'Message one content' },
          {'title':'Message Two',
           'content':'Message Two content' },
          ]
@app.route("/chat")
def chat():
    return render_template("chat.html", messages=messages);

@app.route('/create/' , methods=('GET', 'POST'))
def create():
    if request.method=="POST":
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            messages.append({'title':title,'content':content})
            name = "Bala G"
            return redirect(url_for("chat", messages=name ))
    return render_template("create.html") 


@app.route("/database")
def database():
    return render_template("database.html");

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

  return "success..."