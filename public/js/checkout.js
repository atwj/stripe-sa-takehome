var stripe = Stripe('pk_test_51JgquZFrYPN0ETfkDxQJYYuxnMB7znIdf5gWrwzXekEU2wrEreEpI17rsqIR6USxUePORqdjVAF0ZQDj6IDuk4im00STkouwWY');
(function(){
    'use strict';
    

    var elements = stripe.elements({
        fonts: [
        {
            cssSrc: 'https://fonts.googleapis.com/css?family=Roboto',
        },
        ],
        // Stripe's examples are localized to specific languages, but if
        // you wish to have Elements automatically detect your user's locale,
        // use `locale: 'auto'` instead.
        locale: 'auto'
    });

    var card = elements.create('card', {
        iconStyle: 'solid'
    });

    $(document).ready(function(){
        card.mount('#stripe-card-element');
        var form = document.getElementById('payment-form');
        form.addEventListener('submit', function(ev) {
            ev.preventDefault();
            // If the client secret was rendered server-side as a data-secret attribute
            // on the <form> element, you can retrieve it here by calling `form.dataset.secret`
            stripe.confirmCardPayment(form.dataset.secret, {
                payment_method: {
                    card: card
                }
            }).then(function(result) {
                console.log("Promise complete")
                console.log(result)
                if (result.error) {
                // Show error to your customer (e.g., insufficient funds)
                console.log(result.error.message);
                } else {
                // The payment has been processed!
                if (result.paymentIntent.status === 'succeeded') {
                    // Show a success message to your customer
                    // There's a risk of the customer closing the window before callback
                    // execution. Set up a webhook or plugin to listen for the
                    // payment_intent.succeeded event that handles any business critical
                    // post-payment actions.
                    window.location.href = "/success" + '?pid=' + result.paymentIntent.id
                    
                }
                }
            });
        });
    })
})();

