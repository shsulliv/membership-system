# Membership System
Membership system project for British Computing Society synoptic project.

## Prerequisites for installation:
1. Having Python 2.7 installed. Running the following command in your terminal to see which version of Python you have:
```code
python --version
```
If you do not have Python currently installed, visit the Python site and follow the instructions to install the 2.7 version of the language on your operating system.
2. Having pip installed. Pip already comes bundled with Python version 2.7 and higher, otherwise run the following two commands separately in your terminal:
```code
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```
3. Installing Flask. Flask is the library that this code is using for structuring API routes/requests. Run the following command in your terminal:
```code
pip install Flask
```
4. Install [Postman](https://www.getpostman.com/). While this step is not necessary, it is the application that I used to test the REST API and I highly recommend its friendly UI for testing the functionality of the API’s endpoints.
5. Running the server. Navigate to the project directory that you’ve just downloaded:
```code
cd <path_to_the_project_directory>
```
Now run the following command in your terminal:
```code
python server.py
```
Lastly, following the localhost: link provided in the running server to your browser and play with the API! The routes for the various endpoints are available in server.py.
Note: If you don’t see a crud.lite file in the project directory, it means that the database has not yet been created for this project. To start the database, open the Python interactive shell in your terminal by typing:
```code
python
```
Then, in the Python interactive shell, type in the follow two commands:
```code
>>> from server import db
>>> db.create_all()
```
Press CTRL + d to exit the shell. These commands will have auto-generated a crud.lite file which will serve as your database. The database is now empty, so be sure to create some users over in Postman.
6. Run the unit tests. First, install pytest.
```code
pip install pytest
```
To run the tests associated with this project, run the following command in your terminal:
```code
pytest server_test.py --verbose
```

## API Endpoints available:
- get_user()
- edit_user()
- add_user()
- delete_user()
- get_all()
