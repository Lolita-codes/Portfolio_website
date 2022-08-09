from flask import Flask, render_template, url_for
import smtplib, ssl
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os
from dotenv import load_dotenv
load_dotenv('.env')
import email_validator

app = Flask(__name__)
app.config['APP_SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')
Bootstrap(app)


# Creates the contact form
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField('Email', [validators.email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


# Renders the homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as connection:
            connection.login(user=os.environ['EMAIL'], password=os.environ['PASSWORD'])
            connection.sendmail(
                from_addr=os.environ['email'],
                to_addrs=os.environ['email'],
                msg=f"Subject: New Message\n\nName: {contact_form.name.data}\nEmail address: {contact_form.email.data}\nMessage: {contact_form.message.data}"
            )
        return render_template('index.html', form=contact_form)
    else:
        return render_template('index.html', form=contact_form)


# Renders the resume page
@app.route('/resume')
def check_resume():
    return render_template('resume.html')


app.add_url_rule('/favicon.ico',
                 redirect_to=url_for('static', filename='favicon.ico'))


if __name__ == '__main__':
    app.run(debug=True)
