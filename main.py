from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

# import os
# os.system("pip install Flask-SQLAlchemy")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pythonwork'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Job(db.Model):
    __tablename__ = 'dd'
    Index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)



@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')



@app.route('/vacancy', methods=['GET', 'POST'])
def vacancy():
    if request.method == 'POST':
        search_query = request.form['search_query']
        jobs = Job.query.filter(or_(Job.job.ilike(f'%{search_query}%'),
                                    Job.company.ilike(f'%{search_query}%'),
                                    Job.country.ilike(f'%{search_query}%'),
                                    Job.type.ilike(f'%{search_query}%'))).all()
    else:
        jobs = Job.query.all()

    return render_template('vacancy.html', jobs=jobs)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'you are logged out'


@app.route('/add_vacancy', methods=['GET', 'POST'])
def add_vacancy():
    if request.method == 'POST':
        j = request.form['job']
        com = request.form['company']
        coun = request.form['country']
        t = request.form['type']

        new_job = Job(job=j, company=com, country=coun, type=t)

        db.session.add(new_job)
        db.session.commit()

        flash('Vacancy added successfully!', 'success')

        return redirect(url_for('add_vacancy'))

    return render_template('add_vacancy.html')


if __name__=="__main__":
    app.run(debug=True)


