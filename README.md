# flask_example

## Requirements

- MySQL installed
- Python installed
- Pip installed

## Installation

- In the main directory "flask_example", to install dependencies:

```code
pip install -r requirements.txt
```

- In the main directory "flask_example", to create a fresh database using MySQL, and assuming local defaults user: root, pass: (none):

```code
mysql -u root
source app/db/schema.sql
exit;
```

- To seed from JSON file(s):

```code
py seeds.py
```

## Usage

Default port: 5000

- To create a virtual environment prior to starting the application, then activate the venv:

```code
py -m venv venv
venv\Scripts\activate
```

- To deactivate the virtual environment:

```code
deactivate
```

- In the main directory "flask_example", with the virtual environment running, to run the api application:

```code
flask run
```