## Welcome to simple logistic application

### Prequisition

This application build with Django 5.x.x version and use Python version 3.10.x. Database use SQLite. Deployment use Docker and Nginx as webserver.

### Feature

- Login and register with monolith (use default template engine as UI)
- Login and register with Rest API. Use bearer token authentication
- Simplest CRUD Country and Category for international pricing
- Use Raja Ongkir API for calculate domestic shipping price
- Dump/Import Country and Category data from .csv files (example files inside root dir)
- Searching: country, category and city

### How to run

Best practice always use Python environment. In this case I use Windows 10.

- Pull this repository
- Inside root dir run command `python -m venv venv`
- Activate venv by run `venv/scripts/activate` or if you use Linux based `source venv/bin/activate`
- After venv active, install dependencies with `pip install -r requirements.txt`
- Change directory to `cd logiblue` (where `manage.py` file located)
- Dump Country and Category by run command: `python manage.py dump_country` and `python manage.py dump_category`
- Run migration first by `python manage.py migrate`
- Run application server by `python manage.py runserver`
- Open web-browser and typing `http://localhost:8000`

### Rest API

This application has several Rest APIs endpoint

- Search country GET: `/api/countries?search={keyword}`
- Search category GET: `/api/categories/?country_code={ISO 3166 (3 digits)}&search={keyword}`
- Search destination city GET: `/api/cities/?search={keyword city name}`
- Calculate freight POST: `/api/calculate/` with body:

```
{
    country_code: ISO 3166 (3 digits),
    category_id: id off category,
    destination_id: city id,
    weight: float, in kilogram
}
```
