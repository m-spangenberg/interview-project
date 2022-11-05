# Form Project

As part of the applicant screening process, I have been tasked with completing a small full-stack project. The project touches on frontend web development basics like HTML, CSS and DOM interaction via JavaScript, as well as backend tasks like endpoint routing, form handling and database interactions. More broadly the emphasis is on writing clean, reusable code that respects modern software development standards and best practices. I have been allowed to complete the core requirements outlined in the provided project file in a language and framework of my choice: Python and Flask paired with SQLite as the database.

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

### Instructions

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

Hopefully the website design is self-documenting.