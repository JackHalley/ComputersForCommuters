from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('Email is required!')
            return redirect('/')

        existing_email = Email.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already subscribed!')
            return redirect('/')

        new_email = Email(email=email)
        db.session.add(new_email)
        try:
            db.session.commit()
            flash('Thanks for subscribing!')
        except:
            db.session.rollback()
            flash('An error occurred. Please try again.')

        return redirect('/')
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
