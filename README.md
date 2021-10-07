# About
This is a simple e-commerce application forked from [https://github.com/marko-stripe/sa-takehome-project-python](https://github.com/marko-stripe/sa-takehome-project-python). 
It is essentially a site that allows site users to select a book and pay for it using Stripe's payment gateway. 

As part of the Solution Architect assessment, my task was to integrate Stripe with this application in order 
to provide the payment functionality. The following sections will cover how the application works, how I approached 
this problem and overcome challenges faced in this process before ending it off with a summary on how this application 
could be made more robust. 

# Application Overview

## What's in the box
- The backend service is written in Python using the [Flask framework](https://flask.palletsprojects.com/).
- The frontend is styled with [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/) CSS framework.
- The Payment functionality is provided by Stripe, using the [`PaymentIntents`](https://stripe.com/docs/api/payment_intents) 
API and [Stripe Elements](https://stripe.com/docs/js/elements_object/create_element?type=card) to collect payment details 
and facilitate the payment.

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

Next, I looked into the existing source code to understand how the application was put together. Here are some things that 
I observed:
1. There is a `/checkout` route and `/success` route already defined in `app.py`. This should be where I will implement the server side logic for the payment functionality.
2. The .env file does not seem to be loading the publishable and secret API keys correctly. I will have to fix that.
3. The available book selections are hardcoded into the view. I may want to refactor that later.

### Step 2: Complete the task.
Now that the application is running, I had to figure out the following items:
1) How to use Stripe Elements to render a UI component to capture payment details.
2) Which Stripe API(s) to use in order to faciliate payment on the backend
3) What is the right way to use both Stripe Elements and the various Stripe API(s) together in order faciliate payment.

I decided that I would start by looking at the available guides provided by Stripe. This proved to be extremely helpful
as I found the exact codes needed for this to work. 
Here is the [link](https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements) to the said guide. 

More importantly, I understood how the `PaymentIntent` API was to be used as well as the interactions required between the customer,
client, e-commerce backend and Stripe for a payment to happen.   

![PaymentIntent usage](https://b.stripecdn.com/docs-srv/assets/accept-a-payment-web.3c58b380538c59796acc587164c05365.png)

What I found fascinating was that the second leg of the interaction where the customer had to confirm the payment need 
not go through the server, but directly to Stripe. I believe that this is by design because if the server were to receive card 
information, this would result in security and regulatory challenges that had to be addressed. For example, ensuring that card information was not 
cached or stored server side and ensuring that the application complies with prevailing guidelines like PCI DSS.


### Step 3: Make it work well.
With the help of the [guide](https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements), the implementation 
of the payment feature was quickly completed. 

However, there were certain features that I wanted to add in order to improve the overall experience of purchasing a book on the site. 
1. Adding a spinner when the "pay" button was clicked. It takes about 0.5 to 1 second for the payment to be confirmed, I wanted to let the customer know
that the payment was being processed as soon as the "pay" button was clicked.
2. Handling payment errors (i.e card declined, insufficient balance). In the event when a card is declined, I wanted to set an appropriate
error message informing the customer to try again later.   

### Step 4: Refactor.

### Challenges Faced
There was only one challenge that I faced while implementing the payments feature. I could not retrieve the charge ID from the
result of calling `stripe.confirmCardPayment(...)` in `checkout.js` after the payment has been confirmed.

    stripe.confirmCardPayment(form.dataset.secret, {
        payment_method: {
            card: card
        }
    }).then(function(result) {
        console.log(result.charges) // result.charges not found.         
    })

My immediate suspicions were:
#### 1. There could be a delay between payment confirmation and the creation of a `charge` record.

To test this, I started by checking the payments tab in the Stripe dashbord to see if an event log was available. Sure enough,
there was an event log under the "Event and Logs" section. There I observed that a `charge` is created no more than 2 seconds after the payment is confirmed.
Therefore, to test whether the cause of this issue was due to a delay, I decided to check for the `charge` object only 5 seconds
after the payment has been confirmed (i.e when the javascript Promise was resolved).

    // checkout.js
    stripe.confirmCardPayment(form.dataset.secret, {
        payment_method: {
            card: card
        }
    }).then(function(result) { //When Promise is resolved
        setTimeout(function(){ // Wait for 5000 ms before executing console.log(result.charges)
            console.log(result.charges) 
        }, 5000);        
    })

However, there was still no `charge` object being returned. Thus I concluded that it is likely information about `charge` 
is not being returned at all in this `PaymentIntents` object when using Stripe.js . 

#### 2. Perhaps certain fields were only available depending on whether a publishable API key or secret API key was used.
Now armed with a new hypothesis, I decided to try retrieving the `charge` details using the Python Stripe SDK. To test this,
I left the code implementation in `checkout.js` as is and added an implementation in the `app.py` that would print out the 
`charge` object immediately after payment is confirmed.
    
    // checkout.js
    stripe.confirmCardPayment(form.dataset.secret, {
        payment_method: {
            card: card
        }
    }).then(function(result) { 
        window.location.href = "/success" + '?pid=' + result.paymentIntent.id // calls /success route with the payment intent ID 
        setTimeout(function(){ // Wait for 5000 ms before executing console.log(result.charges)
            console.log(result.charges) // result.charges not found
        }, 5000);        
    })

    # app.py
    # Success route
    @app.route('/success', methods=['GET'])
    def success():
        payment_intent_id = request.args.get('pid') # Retrieves payment intent ID from query parameter
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        print(payment_intent.charges) # charges was FOUND
        return render_template('success.html')

What I found was that the `charge` created upon payment confirmation was retrievable in the Python example, but not in the Javascript example. The only other difference between 
these two SDKs was that the javascript SDK was configured with the publishable API key, while the python SDK was configured with the secret API key. 
Upon checking the documentation for `PaymentIntents` again, I realized that certain fields were annotated with "RETRIEVABLE WITH PUBLISHABLE KEY". I also noticed
that Stripe.js was intended to be used in client-side code exclusively and only accepts the publishable API key. This likely means that the type of API key used
may result in different fields being returned. I belive that this is likely a security related design.

## How do I make this application more robust?
A pragmatic way to scale up this application would be to decouple the front-end code and the backend code. This results in two code bases that
are maintained and deployed separately. The benefits from doing so include:
1. Increased agility and ease of adding new features to either front-end or back-end.
2. The ability to the scale the client-side or server side deployment out or in independently depending on traffic.
3. The ability to add new front-ends (i.e mobile applications) or further decompose the backend for better maintainability and performance (i.e microservices,
event-driven architectures.)


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

