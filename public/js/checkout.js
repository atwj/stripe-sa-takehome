(function(){
    'use strict';
    var elements = stripe.elements({
        fonts: [
        {
            cssSrc: 'https://fonts.googleapis.com/css?family=Roboto',
        },
        ],
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
            document.getElementById("payment-processing-overlay").style.display = "block"
            document.getElementById("payment-error").style.display = "none"
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
                    document.getElementById("payment-processing-overlay").style.display = "none"
                    document.getElementById("payment-error").style.display = "block"
                    console.log(result.error)
                    //Display error pop up.
                } else {
                // The payment has been processed!
                if (result.paymentIntent.status === 'succeeded') {
                    // Show a success message to your customer
                    // There's a risk of the customer closing the window before callback
                    // execution. Set up a webhook or plugin to listen for the
                    // payment_intent.succeeded event that handles any business critical
                    // post-payment actions.
                    // $(document).getElementById("payment-processing-overlay").style.display = "none"
                    window.location.href = "/success" + '?pid=' + result.paymentIntent.id
                    
                }
                }
            });
        });
    })
})();

