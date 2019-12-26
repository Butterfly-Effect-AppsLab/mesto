# mesto
appka pre round 4 team mesto





#########################
# Running Flask app	#
#########################

_____________________________________________________
Windows:

---- Python 3.7. installation required (may need set environmental variable Python.exe from path where python was installed)

0. create directory
1. clone repository from git
	- git clone {githubURL}
2. create virtual environment
	- cmd venv venv in cloned repository
3. activate virtual environment
	- cd venv/Scripts
	- activate
   ------ virtual environment is activated when "(env)" on start of the line
4. install requierd dependencies for the project
	- change directory to project
	- pip install --requirements (this will install all libraries listed in requirements.txt)
5. run flask app
	- set FLASK_APP=application
	- set FLASK_ENV=development (activates real-time in-code changes)
	- flask run
6. app will run on listed localhost and port

___________________________________________________________
MacOS:

1. create directory
2. git clone {githubURL}
3. create virtual environmnet
	- python3 -m venv venv
4. activate: 
	- venv/bin/activate
(you know if activated, in terminal is (venv) in front of user name)
5. instal flask framework
6. pip3 install flask
7. instal sqlAlchemy
8. pip install Flask-SQLAlchemy
9. instal flask restfull
10. pip install Flask-RESTful
11. instal postgres
12. brew install postgresql
	- If you have issues with installing psycopg2 on mac, try run
brew doctor
	- It will find issues in homebrew. I had wrong path for xcode
13. Instal psycopg2
13. pip3 install psycopg2
14. run python app
	- python3 -m flask run
