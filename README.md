# FoxWall

Foxwall is a basic social media api service written with python/django. It's completely open source. Feel free to fork. Also you can contribute. Just create pull request.

## Image From API
&emsp;
![API Image](images/api_service.png)

I used [drf-spectacular](https://github.com/tfranzel/drf-spectacular) for Open API 3.0

&emsp;

## How To Use

### Prerequisites

Currently python and [poetry](https://python-poetry.org/) must be in your system. I'm saying currently because this project will have docker option.

&emsp;
### Using Foxwall

1. Clone this repository.
2. Go to backend folder.
2. Execute `poetry shell` in your terminal.
3. Execute `poetry install` and wait for the messages will done.
4. Execute `python manage.py migrate` for migrating.
5. Execute `python manage.py runserver`. And that's it! Now you are be able to use Foxwall API. For that just go to [localhost:8000](http://127.0.0.1:8000)

> For testing and linting you should execute `poetry install --dev` too.

&emsp;

### Testing

I used pytest for unit testing and e2e testing.

### Trying the tests
Execute `pytest` for testing the app.
For the test coverage please execute `pytest --cov` or `pytest --cov --cov-report=html` if you want html report.

&emsp;

## Database Diagram

How i coded models? Firstly i decided to think about db. For this purpose i created diagram below (with [Db Diagram](https://dbdiagram.io)). That diagram helped a lot. I suggest to create database diagram whenever you start to a backend project.

![Database Diagram](images/diagram.png)


## This is not done yet...

- [ ] Docker configurations.
- [ ] Leave a post as comment to the post.
- [ ] Currently there is not using fields such as last_edited on post. Should make meaningful these fields.
