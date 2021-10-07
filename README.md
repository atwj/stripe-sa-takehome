# About
This is a simple e-commerce application that a customer can use to purchase a book. The payments functionality has been implemented using Stripe's API. This project was forked from [https://github.com/marko-stripe/sa-takehome-project-python](https://github.com/marko-stripe/sa-takehome-project-python)

# Application Overview

## What's in the box
- The backend service is written in Python using the [Flask framework](https://flask.palletsprojects.com/).
- The frontend is styled with [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/) CSS framework.
- Payment functionality is provided by Stripe, using the following APIs:
  - A
  - B
  - C

## How it works

Sequence Diagram
1. Clicking on item (booK)
2. Payment intent is created
3. User is routed to checkout page to complete payment
4. If payment suceeds, route to success page, with payment intent ID in the path parameter.
5. Charge ID is retrieved and shown to user.

## How I approached the problem

### Challenges
1. Unable to get charge ID from success payload in the frontend.
2. 

## How do I scale this up?
1. Decoupling frontend from backend
2. 

## Install and Run
To get started, clone the repository and run pip3 to install dependencies:

```
git clone https://github.com/marko-stripe/sa-takehome-project-python && cd sa-takehome-project-python
pip3 install -r requirements.txt
```

Rename `sample.env` to `.env` and populate it with your Stripe account's test API keys.

Then run the application locally:

```
flask run
```

Navigate to [http://localhost:5000](http://localhost:5000) to view the index page.

