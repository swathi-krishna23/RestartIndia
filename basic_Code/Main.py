from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'the random string'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))




################################  REGISTER  LOGIN  LOGOUT ROUTES ###################################


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = hash(request.form['password'])
        data = User.query.filter_by(username=username,
                                    password=password).first()

        if data is not None:
            session['user'] = data.id
            print(session['user'])
            return redirect(url_for('index'))

        return render_template('incorrectLogin.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(username=request.form['username'],
                        password=hash(request.form['password']))

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


####################################  ROUTES TO DISPLAY #########################################

@app.route('/show')
def show():
    show_user = User.query.all()
    return render_template('show.html', show_user=show_user)




####################################  OTHER ROUTES  #########################################

@app.route('/index')
def index():
    username = User.query.get(session['user']).username
    print(username)
    flash("welcome {}".format(username))
    return render_template('index.html')




######################################### MAIN ####################################


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)