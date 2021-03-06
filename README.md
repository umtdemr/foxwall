# FoxWall

<p align="center">
<img src="https://github.com/umtdemr/foxwall/actions/workflows/django.yml/badge.svg?branch=master">
<a href="https://codecov.io/gh/umtdemr/foxwall">
  <img src="https://codecov.io/gh/umtdemr/foxwall/branch/master/graph/badge.svg?token=WQWCF98A6C"/>
</a>
</p>

Foxwall is a basic social media API service written with python/django. It's completely open source. Feel free to fork. Also pull requests are welcome.

## Screenshot
&emsp;
![API Image](images/api_service.png)

I used [drf-spectacular](https://github.com/tfranzel/drf-spectacular) for Open API 3.0

&emsp;

## How To Use

### Prerequisites

Currently python and any virtual environment package must be in your system. I'm saying currently because this project will have docker option.

&emsp;
### Using Foxwall

1. Clone this repository.
2. Create virtual environment and install packages from requirements.txt file.
4. Execute `python manage.py migrate` for migrating models to database.
5. Execute `python manage.py runserver`. And that's it! Now you are able to use Foxwall API. For that just go to [localhost:8000](http://127.0.0.1:8000)


&emsp;

### Testing

I Used pytest for unit and e2e testing.


### Trying the tests
Execute `pytest` for testing the app.
For the test coverage please execute `pytest --cov` or `pytest --cov --cov-report=html` if you want html report.

&emsp;

## Database Diagram

Before I start to code, I created a database diagram with [dbdiagram.io](https://dbdiagram.io) for how should database look like. That helped me a lot on code process. I suggest to create diagram whenever you start to any project. Not only db diagram, it can be logic diagram, code process diagram, roadmap, etc...

![Database Diagram](images/diagram.png)


## Not done yet...

Obviously, there is things to do.

- [ ] Docker configurations.
- [ ] Leave a post as comment to the post.
- [ ] Currently there are fields that i did not use such as last_edited field on post model. Should make meaningful these fields.
- [x] Fix bio issue after registiration
- [ ] Password reset request
