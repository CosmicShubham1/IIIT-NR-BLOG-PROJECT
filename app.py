from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Updated SQLAlchemy Database URI format
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://WxHtbGLVgNiQThf.root:q6geL4tbDWNSM3Eu@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true'


db = SQLAlchemy(app)

class Blogpost(db.Model):
    __tablename__ = 'blog'  # Ensure it matches your existing table name
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Default to current UTC time
    title = db.Column(db.String(50), nullable=False)
    subtitle = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/delete')
def delete():
    posts = Blogpost.query.order_by(Blogpost.date.desc()).all()
    return render_template('delete.html', posts=posts)

@app.route('/addpost', methods=['POST'])
def addpost():
    date=datetime.now(),  # Current date and time
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    post = Blogpost( title=title, subtitle=subtitle, author=author, content=content)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletepost', methods=['DELETE', 'POST'])
def deletepost():
    post_id = request.form.get("post_id")
    post = Blogpost.query.filter_by(id=post_id).first()

    db.session.delete(post)
    db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()