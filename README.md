# Form Project

As part of the applicant screening process, I have been tasked with completing a small full-stack project. The project touches on frontend web development basics like HTML, CSS and DOM interaction via JavaScript, as well as backend tasks like endpoint routing, form handling and database interactions. More broadly the emphasis is on writing clean, reusable code that respects modern software development standards and best practices. I have been allowed to complete the core requirements outlined in the provided project file in a language and framework of my choice: Python and Flask paired with SQLite as the database.

* The solution must be named: `BCX_{YOUR_FIRSTNAME}_BA_SOL`

## Application Flow

The flow pattern during usage by either an applicant in the questionnaire portal or a privileged user in the admin portal.

![Interview Project Flow Illustration](/readme/interview-project-flow.svg)


## Template Inheritance Diagram

## Questionnaire Flow

## Database Flow

## Database Schema

```sql
```

## Database Models Considerations

The data model below was my proposed solution to driving the form generation in the frontend and still be able to modify the existing form's state while maintaining review capabilities but I ran out of time to normalize and extend the database structure in a way that allows for this sort of decoupling.

```py
class Applicant(db.Model):
    """
    applicants table with email as the requested primary key
    """
    email = db.Column(db.String(64), primary_key=True, unique=True, nullable=False)
    stats = db.relationship('ApplicantStats', back_populates='applicant', uselist=False)

class ApplicantStats(db.Model):
    """
    session statistics for applicants
    in a one-to-one relationship with the Applicant table
    """
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.String, db.ForeignKey('applicant.email'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    state = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer, default="0")
    applicant = db.relationship('Applicant', back_populates='stats')

class User(db.Model, UserMixin):
    """
    superusers table for backend access
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

class FormSession(db.Model):
    """
    state of the the applicant's session
    """
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.String, db.ForeignKey('applicant.email'))
    answer = db.Column(db.String(1024))
    state_id = db.Column(db.Integer, db.ForeignKey('form_state.version'))
    state = db.relationship('FormState', backref='parents')

class FormState(db.Model):
    """
    state of the questionnaire
    in a many-to-one relationship with FormSession
    """
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey("form_question.id"))
    input_id = db.Column(db.Integer, db.ForeignKey("form_input.id"))
    choice_id = db.Column(db.Integer, db.ForeignKey("form_choice.id"))

class FormQuestion(db.Model):
    """
    questions available to form
    """
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256))
    
class FormInput(db.Model):
    """
    input types available to form questions
    currently: input, select, and radio
    """
    id = db.Column(db.Integer, primary_key=True)
    input_type = db.Column(db.String(32))

class FormChoice(db.Model):
    """
    choices available to the input types
    for inputs that require multiple values: radio and select
    """
    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(64))
```

## Deployment

### Docker Instructions

This project has been packaged into a Docker image to showcase what a standard deployment workflow would look like in a development environment. The image is available at TODO:INSERT DOWNLOAD LINK, deploying it in your own environment should be easy as long as you have Docker installed. If you prefer not to use Docker, please use the alternate instructions.

Optional: Build image from source

```bash
docker build --tag forms-project .
```

Deploy container via Docker Run CLI

```bash
# start the container in detached mode with network bound to port 5000 and destroy it on exit
sudo docker run -rm -d -p 5000:5000 --name forms forms-project
# populate the database with forms
sudo 
```

### Alternate Instructions

```bash
# clone this repository
git clone https://github.com/m-spangenberg/interview-project.git forms
cd ./forms
# make sure you have pipenv installed
pip install --user pipenv
# install the needed dependencies from the piplock file
pipenv install 
# or if you prefer use the requirements.txt file
pipenv run flask --app questionnaire --debug run --host=0.0.0.0
```

## Usage

For testing purposes the following accounts are auto-generated when the database is first created. Make use of them to test frontend and backend functionality.

Admin Account

```bash
# username
admin@example.com
# password
adminpassword!
```