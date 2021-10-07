import os
import stripe
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect

from service import book_dao
from model.book import Book

load_dotenv()

# Configure stripe with API key
secret_key = os.environ.get("STRIPE_SECRET_KEY")
publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY")
if secret_key:
	stripe.api_key = secret_key
else:
	raise ValueError("STRIPE_SECRET_KEY not set.")

if publishable_key == None:
	raise ValueError("STRIPE_SECRET_KEY not set.")

app = Flask(__name__, 
	static_url_path='',
	template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
	static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))

# Home route
@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

# Checkout route
@app.route('/checkout', methods=['GET'])
def checkout():
  # Just hardcoding amounts here to avoid using a database
	item = request.args.get('item')
	if item is None:
		return redirect("/", code=302)

	book = book_dao.get_book_by_id(item)

	# Create payment intent since price and item already known
	# Return client_secret as part of checkout.html for it to be used later.
	payment_intent = stripe.PaymentIntent.create(amount=book.amount, currency="SGD")
	return render_template('checkout.html', 
								title=book.title, 
								amount=book.amount, 
								# error=error, 
								client_secret=payment_intent.client_secret,
								publishable_api_key=publishable_key
							)

# Success route
@app.route('/success', methods=['GET'])
def success():
	payment_intent_id = request.args.get('pid')
	if payment_intent_id is None:
		return redirect("/", code=302)

	payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
	return render_template('success.html', amount=payment_intent.amount, charge_id=payment_intent.charges.data[0].id)


if __name__ == '__main__':
	app.run(port=5000, host='0.0.0.0', debug=True)