# rjp-test
Flask / SQLAlchemy API containing wizard characters, potions and spells

## Installation
1. Create a virtual environment, for instance using [pyenv](https://github.com/pyenv/pyenv) (the code has been developed and tested using Python 3.6.10)
2. Enable the virtual environment
3. Run the following command to install the Python libraries (tested to work with pip 18.1):  
   `pip install -r requirements.txt`
4. Run the following command to setup up the database:  
   `python setup.py`

## Run the server
1. Run the following command to run the Flask development server:  
   `flask run`
2. Go to http://127.0.0.1:5000/ to view the Swagger documentation of the API

## Notes
- The results of the endpoint GET /characters can be sorted and filtered

## Tests
- Run the following command to run the tests proving the API is working properly:  
  `pytest`
