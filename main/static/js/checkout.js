//public key
const stripe = Stripe('pk_test_51Mu4qwJ7nO4k2zjUmdALwcbRacCoWOHm77cxD8trueS2ku55wrHSz2bOGPdRaoJSJOzt8UMkJOofoX2vaze1oD6w00LUmhNIjb')

var elements = stripe.elements();
var style = {
base: {
  color: "#000",
  lineHeight: '2.4',
  fontSize: '16px'
}
};

// Handle button clicks and show the respective payment form
function showWechatPay() {
  document.getElementById('wechatpay-content').style.display = 'block';
  document.getElementById('alipay-content').style.display = 'none';
  document.getElementById('card-content').style.display = 'none';
}

function showAlipay() {
  document.getElementById('wechatpay-content').style.display = 'none';
  document.getElementById('alipay-content').style.display = 'block';
  document.getElementById('card-content').style.display = 'none';
}

function showCard() {
  document.getElementById('wechatpay-content').style.display = 'none';
  document.getElementById('alipay-content').style.display = 'none';
  document.getElementById('card-content').style.display = 'block';
}

// Create an instance of the Card Element
const cardElement = stripe.elements().create('card' , { style: style });
cardElement.mount('#card-element');

document.getElementById('submit').addEventListener('click', function (event) {
  event.preventDefault();
  handleCardPayment();
});

document.getElementById('wechat-submit').addEventListener('click', function (event) {
  event.preventDefault();
  handleWechatPay();
});

document.getElementById('alipay-submit').addEventListener('click', function (event) {
  event.preventDefault();
  handleAlipay();
});

// Handle card payment
async function handleCardPayment() {
  // You need to create a PaymentIntent and retrieve the client secret on the server side
  
  const clientSecret = document.getElementById('submit').dataset.secret;
  var custName = document.getElementById("custName").value;
  var custAdd = document.getElementById("custAdd").value;
  var custAdd2 = document.getElementById("custAdd2").value;
  var postCode = document.getElementById("postCode").value;

  const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: cardElement,
      billing_details: {
        address: {
          line1: custAdd,
          line2: custAdd2, 
        },
        name: custName,
      },
    },
  });

  if (error) {
    document.getElementById('card-error').textContent = error.message;
  } else {
    // Payment successful
    document.getElementById('payment-message').classList.remove('hidden');
    document.getElementById('payment-message').textContent = 'Payment succeeded!';
  }
}

// Handle WeChat Pay
async function handleWechatPay() {
  // You need to create a PaymentIntent with WeChat Pay on the server side and retrieve the client secret
  const paymentIntentResponse = await fetch('create_wechat_pay_payment_intent', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      //'X-CSRFToken': CSRF_TOKEN
    },
    body: JSON.stringify({
      name: document.getElementById('custName').value,
      email: document.getElementById('email').value,
      address: {
        line1: document.getElementById('custAdd').value,
        line2: document.getElementById('custAdd2').value,
        state: document.getElementById('state').value,
        postal_code: document.getElementById('postCode').value,
        country: document.getElementById('country').value,
      }
    }),
  });

  const paymentIntentResult = await paymentIntentResponse.json();
  const clientSecret = paymentIntentResult.client_secret;

  const { error, paymentIntent } = await stripe.confirmWechatPayPayment(clientSecret, {
    payment_method_options: {
      wechat_pay: {
        client: 'web',
      },
    },
    return_url: 'http://127.0.0.1:8000/success/', // Replace with your return URL
  });

  if (error) {
    // Display error.message in your UI.
  } else {
    // Redirect to the provided return URL after payment authentication
    window.location.href = paymentIntent.next_action.redirect_to_url.url;
  }
}

// Handle Alipay
async function handleAlipay() {
  // You need to create a PaymentIntent with Alipay on the server side and retrieve the client secret
  const paymentIntentResponse = await fetch('create_alipay_payment_intent', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      //'X-CSRFToken': CSRF_TOKEN
    },
    body: JSON.stringify({
      name: document.getElementById('custName').value,
      email: document.getElementById('email').value,
      address: {
        line1: document.getElementById('custAdd').value,
        line2: document.getElementById('custAdd2').value,
        state: document.getElementById('state').value,
        postal_code: document.getElementById('postCode').value,
        country: document.getElementById('country').value,
      }
    }),
  });

  const paymentIntentResult = await paymentIntentResponse.json();
  const clientSecret = paymentIntentResult.client_secret;

  const { error, paymentIntent } = await stripe.confirmAlipayPayment(clientSecret, {
    return_url: 'http://127.0.0.1:8000/success/', // Replace with your return URL
  });

  if (error) {
    // Display error.message in your UI.
  } else {
    // Redirect to the provided return URL after payment authentication
    window.location.href = paymentIntent.next_action.redirect_to_url.url;
  }
}