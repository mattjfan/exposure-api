# Exposure API
Flask API backend for the Exposure app project to track exposure risks to COVID-19 

## Developing
I'm using python `3.6.8` but any version 3.6+ is probably fine 

From root...

Create a virtual environment
```
python -m venv venv
```

Start your virtual environment

On windows:
```
venv\Scripts\Activate
```

or Linux:
```bash
. venv/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```

Updating requirements (if you need to add packages, make sure they get added to requirements.txt. Easiest way to do this (while in your virtual environment to avoid pushing extraneous dependencies))
```
pip freeze > requirements.txt
```

Running
```
flask run
```

*Note: We have a .env file for a reason. Plz use it thank you*


## Contributing
Contribution guidelines WIP

## Links
Interested in contributing?

- Mobile Frontend Repo (React Native): https://github.com/mattjfan/exposure-app/ 
- Backend Repo (Flask): https://github.com/mattjfan/exposure-api/
- Slack: https://exposurespace.slack.com
