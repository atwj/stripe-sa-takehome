import os
import stripe
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect

load_dotenv()

# Configure stripe with API key
secret_key = os.environ.get("STRIPE_SECRET_KEY")
if secret_key:
	stripe.api_key = secret_key
else:
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

	title = None
	amount = None
	error = None

	if item == '1':
		title = 'The Art of Doing Science and Engineering'
		amount = 2300
	elif item == '2':
		title = 'The Making of Prince of Persia: Journals 1985-1993'
		amount = 2500
	elif item == '3':
		title = 'Working in Public: The Making and Maintenance of Open Source'
		amount = 2800
	else:
		# Included in layout view, feel free to assign error
		error = 'No item selected'

	# Create payment intent since price and item already known
	# Return client_secret as part of checkout.html for it to be used later.
	payment_intent = stripe.PaymentIntent.create(amount=amount,currency="SGD")
	return render_template('checkout.html', title=title, amount=amount, error=error, client_secret=payment_intent.client_secret)

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