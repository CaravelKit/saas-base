# SaaS Boilerplate

This free SaaS boilerplate allows you to create a working SaaS application with minimal efforts. What it already has:

* Email authentication (with email confirmation)
* User registration, login, logout
* Simple user profile page
* Autocreation of tables for users and roles (2 roles are added automatically: User and Admin)
* Autoupdating existing database
* Simple responsive web interface with header, left collapsing menu, central part, and fixed status bar
* Handling 404 and 500 errors


### Features: ###
* Well organized project structure (blueprints/components based)
* Used bleeding edge web technologies
* Allows to add your own features, pages and components quickly

### Technologies/libraries in use: ###
#### Database: ####
* PostgreSQL
#### Backend: ####
* Flask / Python 3 / SQLAlchemy

#### Frontend: #### 
* ES6 JavaScript
* Vue
* Axios

#### Design / templates: ####
* Bootstrap 4
* Fontawesome 5
* SASS / SCSS

#### Project organize: ####
* Webpack 4



## Getting Started

Follow instruction to install, set up and run this boilerplate to start your SaaS quicker.

### Prerequisites

Before we start make sure you have installed Python 3 and Node.js. Please follow the official instructions. Also, you need to have a PostgreSQL database handy. If you don't want to install it you can use ElephantSQL service, they have a free plan: [https://www.elephantsql.com/plans.html](https://www.elephantsql.com/plans.html).


### Installing

1. Download the full zip or pull code from the repository, [here](https://help.github.com/articles/which-remote-url-should-i-use/) you can find full instruction:
```
git clone https://github.com/SaaS-Idea/saas-boilerplate.git
cd saas-boilerplate
```
2. Create a virtual environment (not necessarily but highly recommended):
```
python -m venv venv
```
(First 'venv' is a command, the second one is a new folder for a virtual environment. Or you can call it whatever.)


3. Add necessarily environment variables:
* Find venv/Scripts/activate.bat file, open in a text editor (__Important! Don't use Notepad++ as for some reason it spoils the file.__)
* Add the following variables before _:END_:
	* set FLASK_APP=main
	* set env=dev
	* set "db_url=postgres://user:password@dbhost:port/database"
	* set "secret_key=your_local_secret_key"
	* set "secret_salt=your_local_salt"
	* set mail_server=your_email_server
	* set mail_port=usually_465
	* set "mail_username=your_email"
	* set "mail_password=your_email_password"
	* set "admin_email=admin_email"
* The same folder find deactivate.bat and add the following strings before _:END_:
	* set FLASK_APP=
	* set env=
	* set db_url=
	* set secret_key=
	* set secret_salt=
	* set mail_server=
	* set mail_port=
	* set mail_username=
	* set mail_password=
	* set admin_email=

Note: if you use privateemail.com for your email you can set up the following settings:
```
set "mail_server=mail.privateemail.com"
set "mail_port=465"
```
### Setting up (quick, automate)
Just run the command:
```
init
```
As soon as you see the following info you can open your browser:
```
* Serving Flask app "main"
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
### Setting up (slow, manual)

1. Activate the environment:
```
venv/Scripts/activate.bat
```

2. Move to the venv folder and install Python dependencies:
```
pip install -r requirements.txt
```
If you see some error you definitely have to update your pip:
```
python -m pip install --upgrade pip
```

3. Move back to the folder where your project is. Install webpack/JavaScript dependencies:
```
npm install
```

4. Build the javascript code and styles:
```
npm run dev
```
Note, there is another config, for production that you can run with "npm run prod" - in this version you will get well zipped (but not readable) code.

5. Initialize the database:
```
flask dbinit -c
```

6. Run the app:
```
flask run
```

7. Open a browser and go http://127.0.0.1:5000/. It will show the 404 error page because there is no any route defined for the root. If you see this page it means everything works fine! Feel free to explore, it's your code now!

## How to debug the code
We prefer MS VS Code. It's free and have tons of plugins for any language and framework. We use plugins for Python, Flask, Vue. To debug Python code you need to do some setups:

1. Open settings: File -> Preferences --> Settings
2. In the Workspace settings section add the following data:
```
{
    "python.pythonPath": "path_to_you_venv/Scripts/python.exe",
    "python.venvPath": "path_to_you_venv/Scripts/activate",
    "python.linting.pylintEnabled": false,
}
```
3. Follow [this instructions](https://code.visualstudio.com/docs/python/tutorial-flask#_run-the-app-in-the-debugger) to set up launch.json. In our case you should have something like that:
```
{
	"name": "Python Experimental: Flask",
	"type": "pythonExperimental",
	"request": "launch",
	"module": "flask",
	"env": {
		"FLASK_APP": "main.py"
	},
	"args": [
		"run",
		"--no-debugger",
		"--no-reload"
	   //"dbinit", 
	   //"-u"
	],
	"jinja": true
}
```
4. To start debugging, open the Terminal, activate the environment from there, the save as we did from the command line, then select Debug-->Start debugging.

## How to update the database

Every time when you change something in your models, run the following command to update the database:
```
flask dbinit -u
```
## What does the app look like?
Before you even clone anything it would be nice to show you what eventually you would own. There are 4 screenshots:
* Login
![Login page](https://www.saas-idea.com/static/images/login.png)
* Register
![Register page](https://www.saas-idea.com/static/images/register.png)
* Confirmed
![Confirmed page](https://www.saas-idea.com/static/images/confirmed.png)
* Dashboard
![Dashboard page](https://www.saas-idea.com/static/images/dashboard.png)

## Important note about this free version

This version of our SaaS boilerplate is free and it will NOT have all the features. 

## Authors

[SaaS Idea](https://www.saas-idea.com)

## License

You CAN NOT use this project for any commercial purposes.
This project is licensed under the Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) License - see the [CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/) file for details.
If you are interested in the full-functional version please check our website [www.saas-idea.com](https://www.saas-idea.com) for pricing and conditions.

## Feedback

* If you find a bug please open an issue or drop us a line at [info@saas-idea.com](info@saas-idea.com).