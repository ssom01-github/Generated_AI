
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import openai

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_profiles.db'
db = SQLAlchemy(app)
app.app_context().push()

openai.api_key = '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'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    bio = db.Column(db.Text())
    interests = db.Column(db.String(255))

    def __init__(self, name, email, bio, interests):
        self.name = name
        self.email = email
        self.bio = bio
        self.interests = interests

@app.route("/", methods=['GET', 'POST'])
def profile():
    advice = None  # Initialize advice as None

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        bio = request.form['bio']
        interests = request.form['interests']
        question = request.form['question']

        user = User(name=name, email=email, bio=bio, interests=interests)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Profile created successfully', 'success')
           
        except:
            db.session.rollback()
            flash('Error creating profile', 'error')

        # Generate advice using OpenAI GPT-3
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"I am interested in {interests}. My question is: {question}",
            max_tokens=100,  # Use max_tokens instead of max
        )
        advice = response.choices[0].text  # Store the generated advice

    return render_template('profile.html', advice=advice)
    











if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
