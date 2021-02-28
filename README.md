# Chanakya
The admission flow after answering the test will eventually also be handled inside Chanakya.

## How to Set up & Run?
Here are the steps you need to follow to set up Chanakya.

1. Install MySQL.
2. Create a virtualenv. (`python -m venv /path/to/your/virtualenv`)
3. Activate the virtualenv you just created. (`source /path/to/your/virtualenv/bin/activate`)
4. Make sure that the current directory is the root of the project.
5. Set the required environment variables. (`export FLASK_ENV=development; export CHANAKYA_ENVIRONMENT=development`)
6. Run the development server using `FLASK_APP=src flask run`

**Note: The value of `FLASK_ENV` and `CHANAKYA_ENVIRONMENT` should always be the same otherwise you will get an error. Also the possible values are `development`, `staging` and `production`. These values will decide the config file used from the `src/config` folder. The config files are in .gitginore.**

## How to Migrate the Database?
We are using `flask-migrate` and `sqlalchemy` (through `flask-sqlalchemy`) to handle our MySQL DB. Migrations are stored in the `migrations` folder in the root of this project. We should never make any manual changes to the migrations folder of our projects. All the time the flow would be to make manual changes to the models lying in `models/` directory and then run the migrations script to go about the process of migrations. Here's what it would look like:

1. Make sure your branch is up to date to ensure that any changes you make are the latest ones.
2. Make changes in the model files.
3. Run `flask db migrate`. This will generate migration scripts in the migrations folder.
4. `flask db upgrade` this will upgrade the schema of your DB.

You can read more about the `flask-migrate` documentation [here] (https://flask-migrate.readthedocs.io/en/latest/)
