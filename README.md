# Global CMA

Global CMA project. Comparative properties market analysis.

## Getting Started

These instructions will aid you in installing the project on development or live environment. For testing and development purposes.

The data required for the project to fully function are not included in the repository.

## Installing

### Preparation

Install Python 3

Apply virtual environment if required. Please consult python documnetation for this step.

### Installing Flask app

Navigate to the Flask app
```
$ cd appflask
```

Install project dependencies

Note, before installing the project dependencies, first you have to run **PDF parser** dependencies 
(see specified section below) 
```
(venv)$ pip install -r requirements.txt
```

Copy the example environment file
```
(venv)$ cp env.example .env
```

Open and edit the environment values to reflect your server's configuration
```
(venv)$ vim .env
```

### Initial Database
You can either navigate to `sample_database` and go through README to restore
a recent database dump with sample data, or create a fresh new database using the instructions
below:
```
(venv)$ python3 manage.py db create
```

Create an administrator account
```
(venv)$ python3 manage.py user adduser
```

Drop/Create/Refresh GIN indexes in 'property' table
```
(venv)$ python3 manage.py drop_gin_indexes
(venv)$ python3 manage.py create_gin_indexes
(venv)$ python3 manage.py refresh_gin_indexes
```

### Running

Configure WSGI of your choice for production environment. Consult WSGI documentation for details.


To run in development environment, navigate to `appflask` directory and execute:
```
(venv)$ export FLASK_APP=app
(venv)$ export FLASK_ENV=development
(venv)$ flask run
```

To run in gcmaportal development environment, navigate to `appflask` directory and execute:
```
(venv)$ export FLASK_APP=gcmaportal_importer.py
(venv)$ export FLASK_ENV=development
(venv)$ flask run
```

## Vue Front-end integration
Vue app is separate front-end part of the app that communicate with server via REST API. [Vue](https://vuejs.org/v2/guide/) is javascript framework and it requires [Node.js](https://nodejs.org/en/) and [npm](https://www.npmjs.com) to compile. If you doesn't have Node.js, please follow this instructions on [https://nodejs.org/en/](https://nodejs.org/en/)

When you get Node.js npm is already installed.
To check is Node installed run `node -v`
It should return current version like this:
```
v8.10.0
```

### Compiling vue front-end
- 1) Navigate to vueapp folder `cd vueapp`
- 2) Install all dependencies `npm install` 
- 3) Run build process from vue source files `npm run build`
This step will compile source code in html, js, css files and move them in flask app templates and static folder.
- 4) Restart flask server
- 5) Enjoy 🎉

### Serve vue front-end on dev server
To run vue on dev live server you should allow CORS request by flask app. **NOTE:** Do not allow CORS on prod server. Steps:

- 1) change env variable `FLASK_CORS=True` (default `False`)
- 2) restart flask server
- 3) in vueapp directory run `npm run serve`

This should run node.js server with vue app that makes requests to backend. Please also note, that both servers should be located on `127.0.0.1` host for authorization reason: it uses auth cookies created by flask server.

## Contributing

Please follow the project's design to the best of your capability. Below are instructions for the tools every contributor should be aware of and use them accordingly:

### Database Migrations
Module `Flask-Migrate` (that is a configured Alembic) is used within the project.

Whenever you make a modification to the Database structure, please create a migration
file and add it to the repository.

Other developers and servers can then upgrade their databases to the latest schema
using the generated migrations.

You will mostly use these commands with regards to database migrations:
```
$ flask db migrate  # to create new migrations
$ flask db upgrade # to upgrade your local database using the migration files
```

### Language and localization
We are currently using `python babel` to maintain a high quality of the language used.
Not a single word should be printed from within the code files. Every phrase is extracted by `babel` and is stored in the `translations` folder.

As a contributor, your responsibility is to continue this design choice.
The workflow is next:
1. Add new phrases in the code / html templates
2. Create POT file
3. Update Translations
4. Compile Translations

#### Add new phrases in the code / html templates
Every time a phrase needs to be printed to any output (a webpage, console, PDF report, email, etc) wrap it with gettext function as in the following python example:
```
hello_output = gettext(u'hello: %(name)s', name='Bob')
apples_output = ngettext(u'%(num)s Apple', u'%(num)s Apples', number_of_apples)
```
For the HTML templates:
```
<h1>{{ gettext('Hello World') }}</h1>
```
You are advised to use `lazy_gettext` method when translating outside of the http scope.

Other examples can be found by inspecting project's files.

#### Create POT file
Once you have added the new phrases, we need to update the files responsible for translating. The next command will extract all phrases used in the code and templates.
```
(venv)$ python3 manage.py babel create_pot
```

#### Update Translations
Now updates the already existing translations file with new phrases available from the POT.
```
(venv)$ python3 manage.py babel update_translations
```

#### Compile Translations
```
(venv)$ python3 manage.py babel compile_translations
```

### Style Guide
Please follow [Google's python style guide](https://google.github.io/styleguide/pyguide.html) and use [this snippet](https://gitlab.com/alandarev/globalcma/snippets/1916988) as an example for
how we expect the code to look like.
A few generic points:
* Four spaces as tabulation.
* pep8 is configured as part of the CI/CD pipeline. I.e., every commit is verified for the python style using pep8.
* pyflakes is also enabled in CI/CD pipeline to verify all imports are used.
A contributor is advised to manually run the style guidelines tests before commits:
```
(venv)$ flake8 --max-line-length 120 ./appflask
```

### PDF Generation
For generating pdf, weasyprint library have to be installed:

```
(venv)$ pip install weasyprint
```
Note, that have to be installed not pip dependencies: https://weasyprint.readthedocs.io/en/stable/install.html  

### QR Code Generation & Reading

To decode scan and read a qr code, pyzbar library require to be installed: 

Mac OS X:
```
brew install zbar
```

Linux:
```
sudo apt-get install libzbar0
```

To read qr code from .pdf files using `pdf2image` package, dependency `poppler` have to be installed:

Mac OS X:
```
brew install poppler
```

Linux:
```
sudo apt-get install -y poppler-utils
```

## PDF parser

Assessment files parsed using pdftotext
Please refer for dependency installation 
https://github.com/jalan/pdftotext

__Note:__ There is a dependncy of `pdftotext` package to `poppler` for OS X. Run `brew install poppler` to resolve the dependency. Also `pip install pdftotext` may fail, try with `$ CPPFLAGS="-std=c++11" pip install pdftotext`.

### Redis firing up
Please refer to 
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs
Section named `Using RQ`
Start rq worker with name `globalcma-tasks`

### Merge clients
To merge two or more clients by `email address` run followed cli command:

```
(venv)$ flask case_management merge_email_clients jev@alandarev.com --drop_duplicated
```

Note, that `drop_duplicated` option is optional. 
 

### Get html and pdf pages as evidence for broward
To save evidence page from broward web.bcpa.net page please run 
```
$ flask case_management broward_evidence <apn>
```
for example 
```
$ flask case_management broward_evidence 514209054050
```
You will get folder /globalcma/appflask/storage/evidence/514209054050
with pdf and html page


## Tips
There is a `manage.py` file inside `appflask` folder that may come handy at times.

For example, you are able to open the shell iside Flask application context using next command:
```
(venv)$ python3 manage.py shell
```

Displaying help:
```
(venv)$ python3 manage.py --help
```

For babel usage:
```
(venv)$ python3 manage.py babel help
```

## For processing input/writing data to database
```
$ cd globalcma/appflask
$ flask fill_sample <county_name> <table_name>
for example:
$ flask fill_sample nassau property
will write input data to the property database
before invoking script please make sure you have source input data
located at its designated location
for example:
appflask/app/data_import/src/nassau/property/residential.asc
appflask/app/data_import/src/nassau/assessment/final/TX451TWN1RS18400.TXT
appflask/app/data_import/src/nassau/sale/2816_CUR.CSV

For nassau assessment you need to specify options:
To get csv data
$ flask fill_sample nassau assessment --csv 
To persist data into database
$ flask fill_sample nassau assessment --persist

To process and store property data for Suffolk 
$ flask fill_sample suffolk property --persist
Please note data will be stored with x and y coordinates instead of latitude and longitude.
To update suffolk records with valid latitude and longitude please visit
http://opendata.suffolkcountyny.gov/datasets/land-use-2016?geometry=-73.083%2C40.770%2C-72.631%2C40.860&page=11
from downloads section get full dataset shapefile.
It should be named like `Land_Use__2016.zip`. Store the zip file under 
../globalcma/appflask/app/data_import/src/suffolk/property
Make sure suffolk properties successfully stored in database then run:
$ flask fill_sample suffolk gis --persist
```

### Update on Nassau property and assessment parser and Broward parser
For faster parsing please use sql commands. 
Download data_source schema from:
https://drive.google.com/file/d/1hYqLYBuk46m0LOwgVp_0EAV7GyMkxS1a/view?usp=sharing

Download helper schema from:
https://drive.google.com/file/d/1NyNzFWcQ9w6eIx1behrT6klF5sa2vgJj/view?usp=sharing

Restore schemas using sample command as below:
```shell script
$ pg_restore --dbname=test_globalcma --format=c -O -x --schema=\"data_source\" --file=/Users/iammashed/projects/globalcma/dumps/data_source.bak --username=globalcma --host=localhost --port=5432
```
Schemas contains broward and nassau tables generated by importing source files.
Run below files in sql console for parsing of nassau and broward respectively:
reparse_nassau.sql
reparse_broward.sql



For property photos
```
To persist photo names into database
$ flask fill_sample photos
Database table propery_photo will be updated with names from s3 bucket

To choose best photo by latest photo date run
$ flask fill_sample choose_best_photo
```

For openstreetmap data 
```
Please follow this guide to import road data into postgres database
https://www.compose.com/articles/geofile-using-openstreetmap-data-in-compose-postgresql-2/
```

To catch email bounces
```
Amazon ses -> identity management -> Domains
Bounce Notifications SNS Topic: set arn created at sns topic
Complaint Notifications SNS Topic: set arn created at sns topic

create ses configuration set
https://medium.com/@krishankantsinghal/how-to-handle-bounce-complaint-and-rejection-from-amazon-ses-using-lambda-and-serverless-f5d70c98c765

https://medium.com/quick-code/how-to-handling-bounced-and-complaint-notification-in-aws-within-15-minutes-827972207484

python code from 
https://medium.com/@MicroPyramid/amazon-ses-handling-bounces-and-complaints-728425c30b71

Note we are using only SNS. (no SQS)
```

To generate pdf emails
```
For linux
sudo apt-get install wkhtmltopdf

Then apply all steps described here.
https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server#debianubuntu

For Macos
brew install Caskroom/cask/wkhtmltopdf
```

To sign pdf we need to install pdftk binary
```
For Ubuntu
$ sudo snap install pdftk
$ sudo ln -s /snap/pdftk/current/usr/bin/pdftk /usr/bin/pdftk

```

To download broward evidence as pdf
For Ubuntu
```bash
$ sudo apt-get install chromium-browser
```

## License
All rights reseved by the rightful owner of the project.

## CONFIDENTIALITY NOTICE
The contents of this repository are intended solely for the authorized project contributors
and the key stakeholders of the project. The content of this project  may contain confidential 
and/or privileged information and may be legally protected from
disclosure. If you are not the intended recipient of this intellectual property or their agent, or
you received this property in error, please immediately alert the repository owner and then delete
any copies you may posses. If you are not the intended recipient, you are hereby
notified that any use, dissemination, copying, or storage of this intellectual property is
strictly prohibited. 





