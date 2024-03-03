# coffee-hunter-100

Coffee Hunter 100 is a field note application for recording the wonderful world of coffee.

## Development Notes

NA

## Dummy Data

**Bean**

Santa Rita

Colombia

Caturra

Washed

Light Roast

---

Don Angel

Guatemala

Caturra

Washed

Light Roast

---

Alma Pineda SL-28

Honduras

SL-28

Natural

Light Roast

---

Luz Dary Burbano

Colombia

Castillo

Washed

Light Roast

## Running Tests

To run _all tests_, run the following from the root project directory:

`python -m unittest discover`

To run _all tests from a single file_, run the following:

`python -m unittest ch_100_app.main.tests`

To run _one specific test_, un the following:

`python -m unittest ch_100_app.main.tests.AuthTests.test_signup`

### Reference

#### Virtual Environments

Create Python3 Virtual Environment:

`python3 -m venv env`

Activate Virtual Environment:

`source env/bin/activate`

Deactivate Virtual Environment:

`deactivate`

Remove Virtual Environment:

`sudo em -rf venv`

#### Requirements.txt

Automagically create a requirements.txt file:

`pip3 freeze > requirements.txt`

Automagically install all packages inside requirements.txt file:

`pip3 install -r requirements.txt`
