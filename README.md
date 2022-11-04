# Form Project

As part of the applicant screening process, I have been tasked with completing a small full-stack project. The project touches on frontend web development basics like HTML, CSS and DOM interaction via JavaScript, as well as backend tasks like endpoint routing, form handling and database interactions. More broadly the emphasis is on writing clean, reusable code that respects modern software development standards and best practices. I have been allowed to complete the core requirements outlined in the provided project file in a language and framework of my choice: Python and Flask paired with SQLite as the database.

## Project Constraints

* The solution must be named: `BCX_{YOUR_FIRSTNAME}_BA_SOL`
* The database must be named: `CX_{YOUR_FIRSTNAME}_BA_DB`
* Project must tbe shared with the hiring manager and cc'd team members via [WeTransfer](https://wetransfer.com/)

## Project Specification

### Design Guidelines

  * **Question 1**: Where did you hear from us, and what do you think will make you a
great asset to the BCX Business Application Department?
    * Respond text characters max length 1024

  * **Question 2**: How many software solutions did you write in your life?
    * Respond with options: 1 to 5, 6 -25, 26 -100, 101 +

  * **Question 3**: Was it fun building a website for an interview?
    * Response with Yes/No

  * **Question Form Area Bonus Criteria**
    * Add a timer that ends the user’s question form session after a [x] period.

**Backend Portal Area**

* Allow admin to review question form submissions
* Add button on each question form entry to export the question form with user answers to JSON.
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

## Questionnaire Flow

## Database Flow

## Database Schema

```sql
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