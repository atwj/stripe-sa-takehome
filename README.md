# About
This is a simple e-commerce application forked from [https://github.com/marko-stripe/sa-takehome-project-python](https://github.com/marko-stripe/sa-takehome-project-python). It is essentially an site that allows site users to select a book and pay for it using Stripe's payment gateway. 

As part of the Solution Architect assessment, my task was to integrate Stripe with this application in order to provide the payment functionality. The following sections will cover how the application works, how I approached this problem and overcome challenges faced in this process before ending it off with a summary on how this application could be made more robust. 

# Application Overview

## What's in the box
- The backend service is written in Python using the [Flask framework](https://flask.palletsprojects.com/).
- The frontend is styled with [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/) CSS framework.
- The Payment functionality is provided by Stripe, using the [`PaymentIntents`](https://stripe.com/docs/api/payment_intents) API and [Stripe Elements](https://stripe.com/docs/js/elements_object/create_element?type=card) to collect payment details and facilitate the transaction.

## How it works

Sequence Diagram
1. User clicks on a book to purchase.
2. This makes a GET /checkout?item=book_id to the backend
3. Backend creates a `PaymentIntent` object using Stripe's SDK with the amount and default currency (SGD).
3. Backend returns a checkout page (checkout.html) displaying the selected book and price, with the PaymentIntent client secret embedded in the form to faciliate the transaction.
4. User enters credit card details and confirms payment with stripe APIs
5. If payment succeeds, redirect user to success.html with the payment intent identifier. 
6. E-commerce backend uses the payment intent identifier to retrieve the corresponding `PaymentIntent`, retrieves the charge identifier, amount and returns it in the success.html page.

## How I approached the problem

### Step 1: Establish a baseline.
My first priority was to get the application to work as-is. I pulled the starter project from GitHub and 
followed the instructions (installing dependencies, retrieving the test API keys from stripe, etc) to start the application.

Immediately, I noticed that the payment feature was not in place and made a mental note to implement that in due course.

Next, I looked into the existing source code to understand how the application was put together. Here are some things that I observed:
1. There is a `/checkout` route and `/success` route already defined in `app.py`. This should be where I will implement the server side logic for the payment functionality.
2. The .env file does not seem to be loading the publishable and secret API keys correctly. I will have to fix that.
3. The available book selections are hardcoded into the view. I may want to refactor that later.

### Step 2: Complete the task.
Now that the application is running, I had to figure out the following items:
1) How to use Stripe Elements to render a UI component to capture payment details.
2) Which Stripe API(s) to use in order to faciliate payment on the backend
3) What is the right way to use both Stripe Elements and the various Stripe API(s) together in order faciliate payment.

I decided that I would start by looking at the available guides provided by Stripe. This proved to be extremely helpful
as I found the exact codes needed for this to work. Here is the [link](https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements) 
to the said guide. 

Moreover, I understood how the `PaymentIntent` API was to be used as well as the interactions required between the customer,
client, e-commerce backend and Stripe for a payment to happen.

![PaymentIntent usage](https://b.stripecdn.com/docs-srv/assets/accept-a-payment-web.3c58b380538c59796acc587164c05365.png)

### Step 3: Make it work well.
With the help of the [guide](https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements), the implementation 
of the payment feature was quickly completed. 

However, there were certain features that I wanted to add in order to improve the overall experience of purchasing a book on the site. 
1. Adding a spinner when the "pay" button was clicked. It takes about 0.5 to 1 second for the payment to be confirmed, I wanted to let the customer know
that the payment was being processed as soon as the "pay" button was clicked.
2. Handling payment errors (i.e card declined, insufficient balance). In the event when a card is declined, I wanted to set an appropriate
error message informing the customer to try again later.   

### Step 4: Refactor.

### Challenges
1. Unable to get charge ID from success payload in the frontend.
2. 

## How do I scale this up?
1. Decoupling frontend from backend


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

