from flask import Flask, render_template,request, jsonify,session
from flask_wtf import FlaskForm
from wtforms import FileField,StringField
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'some$3cretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://icmwuvgxqphskl:29518807a50b98eff4637464f45393efd41a9e80b3dff925af7c55e28e967b28@ec2-54-210-128-153.compute-1.amazonaws.com:5432/d9u7e52sn8k5ti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_IMAGES_DEST']= "static/"
images = UploadSet('images',IMAGES)
configure_uploads(app,images)
db = SQLAlchemy(app)

class EmailPasswordForm(FlaskForm):
    email = StringField('Email', )
    fname = StringField('First Name')
    lname = StringField('Last Name')
    location = StringField('Location')
    gender = StringField('Gender')
    biography = StringField('Biography')
    picture = FileField('image')    

class Users(db.Model):
    __tablename__ = "user_profiles"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    password = db.Column(db.String(120))
    email = db.Column(db.String(120))
    location = db.Column(db.String(120))
    biography = db.Column(db.String(255))
    profile_photo = db.Column(db.String(255))
    joined_on = db.Column(db.String(255))
    def __init__(self, first_name, last_name,username,password, gender, email, location,
                 biography, photo):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = photo
        self.joined_on = format_date_joined()
class Posts(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    photo = db.Column(db.String(255))
    caption = db.Column(db.String(255))
    created_on = db.Column(db.String(255))
    def __init__(self,id,user_id,photo,caption,created_on):
        self.user_id=user_id
        self.photo=photo
        self.caption=caption
        self.created_on= format_date_joined()
class Likes(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    def __init__(self,id,user_id,post_id):
        self.user_id=user_id
        self.post_id=post_id
class Follows(db.Model):
    __tablename__ = "follows"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    follower_id = db.Column(db.Integer)
    def __init__(self,id,user_id,follower_id):
        self.follower_id=follower_id
        self.user_id=user_id
        def __repr__(self):
            return self.id
            
db.create_all()

@app.route('/test', methods=['GET']) 
def api_test():
    return jsonify({"username":session['username'],"password":session['password']})

@app.route('/api/users/register', methods=['POST','GET']) 
def api_register():
    content=request.json
    data=Users(content['first_name'], content['last_name'],content['username'],content['password'], content['gender'], content['email'], content['location'],
                 content['biography'], content['photo'])
    db.session.add(data)
    db.session.flush()
    db.session.commit()
    return jsonify({"message:":"User successfully registered"})
    
@app.route('/api/auth/login', methods=['POST']) 
def api_login():
    content=request.json
    users = Users.query.all()
    for user in users:
        if user.username==content['username'] and user.password==content['password'] :
            session['username']=content['username']
            session['password']=content['password']
            return jsonify({"message:":"User successfully logged in"})
    return jsonify({"message":"User login failed"})
    
@app.route('/api/auth/logout', methods=['GET']) 
def api_logout():
    session.pop('username', None)
    session.pop('password', None)
    return jsonify({"message:":"User successfully logged out"})

@app.route('/api/users/<string:id>/posts', methods=['POST','GET']) 
def api_posts(id):
    dataJson = []
    posts = Posts.query.all()
    if request.method == "POST":
            content=request.json
            data=Posts(0,id,content['photo'],content['caption'],format_date_joined())
            db.session.add(data)
            db.session.flush()
            db.session.commit()
            return jsonify({"message:":"Post successfully added"})

    if request.method == "GET":
        for post in posts:
            if post.user_id==id:
                dataJson.append({
                'id': post.id,
                'user_id': post.user_id,
                'photo': post.photo,
                'caption': post.caption,
                'created_on': post.created_on,
            })            
        return jsonify(dataJson)

@app.route('/api/users/<string:id>/follow', methods=['POST']) 
def api_follow(id):
    content=request.json
    data=Follows(0,content['user_id'],content['follower_id'])
    db.session.add(data)
    db.session.flush()
    db.session.commit()    
    return jsonify({"message:":"successfully followed user"})
    
@app.route('/api/posts', methods=['GET']) 
def api_all_posts():
    dataJson = []
    posts = Posts.query.all()
    for post in posts:
        dataJson.append({
        'id': post.id,
        'user_id': post.user_id,
        'photo': post.photo,
        'caption': post.caption,
        'created_on': post.created_on,
        })            
    return jsonify(dataJson)
    
@app.route('/api/posts/<string:id>/like', methods=['POST']) 
def api_like(id):
   content=request.json
   data=Likes(0,content['user_id'],content['post_id'])
   db.session.add(data)
   db.session.flush()
   db.session.commit()    
   return jsonify({"message:":"successfully followed user"})
    
def format_date_joined():
    import datetime
    now = datetime.datetime.now()  # today's date
    date_joined = now  # a specific date
    return date_joined.strftime("%B %V, %Y")


@app.route('/add', methods=['POST','GET']) 
def profile_add():
    PhotoForm = EmailPasswordForm()
    if request.method == 'POST':
        picture=PhotoForm.picture.data
        print(picture)
        filename = images.save(PhotoForm.picture.data)
        filename= filename
        data=User(1,PhotoForm.fname.data,PhotoForm.lname.data,PhotoForm.gender.data,PhotoForm.email.data,PhotoForm.biography.data,filename)
        db.session.add(data)
        db.session.flush()
        db.session.commit()
        return profiles()
    if request.method == 'GET':
        return render_template("addUser.html",form=PhotoForm)
    return "Form not validated"    


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)