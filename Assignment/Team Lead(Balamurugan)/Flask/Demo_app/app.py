from flask import Flask, url_for,render_template,request,config,session,make_response,abort,redirect,flash;
from markupsafe import escape;

app = Flask(__name__);
app.config['SECRET_KEY'] = 'the secret key'

# @app.route("/post/<int:post_id>")
# def post(post_id):
#     return f"Post {escape(post_id)} Integer"

# @app.route("/projects/")
# def projects():
#     return "Projects/"


@app.route("/")
def index():
    return render_template("index.html");

@app.route("/users/")
def users():
    return render_template("profile.html")

@app.route("/users/<username>")
def profile(username):
    return render_template("profile.html", username=username);

@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"),404

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
