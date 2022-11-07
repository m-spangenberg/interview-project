# syntax=docker/dockerfile:1

# we're pulling down the lastest python image for our build
# since I'm on a Linux machine, it'll default to an AMD64 Linux platform tag

FROM python:latest

# let's set the relative path inside our container
# this is where our project files will be located

WORKDIR /form_app

# now we prep our environment by copying over our dependency file

COPY requirements.txt requirements.txt

# and install all the required dependencies inside the container image

RUN pip3 install -r requirements.txt

# let's copy the rest of the files, our .dockerignore file will keep things tidy

COPY . .

# and then set the instructions needed to run Flask with Python when the container starts

CMD [ "python3", "-m" , "flask", "--app", "questionnaire", "--debug", "run", "--host=0.0.0.0"]