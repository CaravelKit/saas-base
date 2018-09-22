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
git remote add origin https://github.com/SaaS-Idea/saas-boilerplate.git
```
2. Create a virtual environment (not necessarily but highly recommended):
```
python -m venv venv
```
(First 'venv' is a command, the second one is a new folder for a virtual environment. Or you can call it whatever.)

3. Move to the venv folder and install Python dependencies:
```
cd venv
pip install -r requirements.txt
```
4. Add necessarily environment variables:
* Find venv/Scripts/activate.bat file, open in a text editor (__Important! Don't use Notepad++ as for some reason it spoils the file.__)
* Add the following variables before _:END_:
	* set FLASK_APP=main
	* set env=dev
	* set "db_url=postgres://user:password@dbhost:port/database"
	* set "secret_key=local_secret_key"
	* set "secret_salt=local_salt"
	* set "mail_username=your_email"
	* set "mail_password=your_email_password"
	* set "admin_email=admin_email"
* The same folder find deactivate.bat and add the following strings before _:END_:
	* set FLASK_APP=
	* set env=
	* set db_url=
	* set secret_key=
	* set secret_salt=
	* set mail_username=
	* set mail_password=
	* set admin_email=


## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc