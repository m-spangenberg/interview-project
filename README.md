# Form Project

As part of the applicant screening process, I have been tasked with completing a small full-stack project over the course of 72 hours. The project touches on frontend web development basics like HTML, CSS and DOM interaction via JavaScript, as well as backend tasks like endpoint routing, form handling and database interactions. More broadly the emphasis is on writing clean, reusable code that respects modern software development standards and best practices. I have been allowed to complete the core requirements outlined in the provided project file in a language and framework of my choice: Python and Flask paired with SQLite as the database.

## Evaluation

The project will be evaluated on the following criteria:

* Code Reusability
  * How modular is the codebase and can portions of it be reused easily?
* Code Maintenance
  * How difficult is it to keep the code maintained over time?
* Code Documentation
  * How well are features and design choices documented in the codebase?
* Object Orientation
  * To what degree is OOP being implemented to leverage the benefits of instantiation and inheritance?
* Database Design
  * How well thought out is the DB schema, are good practices being implemented in the design?
* Generics
  * How flexible are your functions and classes and can they handle mixed types?
* Method Constructions
  * Do you make use of constructors?
* MVC Implementation
  * Are you making full use of the Mode-View-Controller architecture pattern?
* Code Structure and Architecture
  * How understandable and neat is your codebase's layout and the project's structure?
* Polymorphism
  * Are you correctly implementing parent-child inheritance?

The subheadings above are my interpretations of the evaluation criteria in relation to Python and the Flask framework.

## Project Constraints

* The solution must be named: `BCX_{YOUR_FIRSTNAME}_BA_SOL`
  * Solutions are unique to Visual Studio C# projects
  * Alternatively, use as the name for the project folder
* The database must be named: `CX_{YOUR_FIRSTNAME}_BA_DB`
* Project must tbe shared with the hiring manager and cc'd team members via [WeTransfer](https://wetransfer.com/)
* The project must be submitted before the **72 hour** deadline

## Project Specification

### Goal

Create an internal web site that a user can access in order to complete a series of interview questions. The answers given by an applicant should be stored in a database, and be uniquely identifiable by the user's email address.

### Design Guidelines

**General Specification**

* Avoid static data for questions forms, questions, and answers
* Users submitted data should be tracked with a unique identifier (email).
* The solution must be a [question form](https://www.surveymonkey.com/mp/survey-vs-questionnaire/), not a survey.

**Question Form Area**

* Use appropriate input controls for questions answers.
* Allow user to input their email before starting the question form
* Question that needs to be configured are the following:

  * **Question 1**: Where did you hear from us, and what do you think will make you a
great asset to the BCX Business Application Department?
    * Respond text characters max length 1024

  * **Question 2**: How many software solutions did you write in your life?
    * Respond with options: 1 to 5, 6 -25, 26 -100, 101 +

  * **Question 3**: Was it fun building a website for an interview?
    * Response with Yes/No

  * **Question Form Area Bonus Criteria**
    * Add a timer that ends the user’s question form session after a [x] period.
    * Render all website styles look and feel in a single CSS theme class.

**Backend Portal Area**

* Allow access to a separate backend admin portal area.
* No authentication required, just add a button anywhere to access this area
* Allow admin to review question form submissions
* Add button on each question form entry to export the question form with user answers
to JSON.

  * **Backend Portal Area Bonus Criteria**
    * Add authentication for an admin user. i.e. username and password
    * Statistics reports on how long the user takes to complete the survey.
    * Allow admin to add more questions and answers to question form.

## Application Flow

The flow pattern during usage by either an applicant in the questionnaire portal or a privileged user in the admin portal.

![Interview Project Flow Illustration](/readme/interview-project-flow.svg)


## Template Inheritance Diagram

```bash
Questionnaire Project
│
├── 404.html
├── 500.html
├── build.html
├── confirm.html
├── elements
│   ├── base.html
│   ├── footer.html
│   ├── form_row.html
│   └── nav.html
├── form.html
├── forms.html
├── index.html
└── review.html
```

## Database Schema

```sql
```

## Extras

Some things I had extra time for:

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
pipenv run python app.py
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

User Account

```bash
# username
dummy@example.com
# password
dummypassword!
```