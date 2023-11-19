// to get current year
function getYear() {
    try {
        var currentDate = new Date();
        var currentYear = currentDate.getFullYear();
        document.querySelector("#displayYear").innerHTML = currentYear;
    } catch (error) {}
}

getYear();


/** google_map js **/
function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

var updateBtns = document.getElementsByClassName('update-cart')

for (i=0; i<updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('Product: ', productId, 'Action: ',action)

        console.log('USER: ', user)

        if (user == 'AnonymousUser') {
            addCookieItem(productId,action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productID, action) {
    console.log("user is not authenticated")
    // var cart = JSON.parse(getCookie('cart'))

    if (action == 'add'){
        if (cart[productID] == undefined){
            cart[productID] = {"quantity":1}
        } else {
            cart[productID]["quantity"] += 1
        }
    } else if (action == 'remove') {
        cart[productID]["quantity"] -= 1
        if (cart[productID]["quantity"] <= 0){
            delete cart(productID)
        }
    } else if (action == 'allremove') { 
        if (cart.hasOwnProperty(productID)) {
            delete cart[productID];
        }
    }
    console.log("cart:",cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId, action) {
    console.log('user is authenticated, sending data...')
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('DATA: ', data)
        location.reload()
    })
}

try {
    if (ORDER_SHIPPING == 'False') {
        document.getElementById("user-address").innerHTML = ''
    }
    
    if (user != 'AnonymousUser') {
        document.getElementById("user-info").innerHTML = ''
    }
    
    if (ORDER_SHIPPING == 'False' && user != 'AnonymousUser') {
        document.getElementById('form-submit').classList.add('hidden')
        document.getElementById('payment-info').classList.remove('hidden')
    }
    
    var form = document.getElementById('form')
    
    form.addEventListener('submit', function(e){
        e.preventDefault()
        document.getElementById('form').classList.add('hidden')
        document.getElementById('form-submit').classList.add('hidden')
        document.getElementById('payment-info').classList.remove('hidden')
        document.getElementById('summary-block').classList.add('hidden')
    })
    
    var makepayment = document.getElementById('form-submit')
    
    makepayment.addEventListener('click', function(e) {
        submitFormData()
    })
    
    function submitFormData(params) {
        console.log("Payment Done")
        var userFormData = {
            'fname': null,
            'email': null,
            'total': ORDER_TOTAL,
        }
    
        var shippingInfo = {
            'address': null,
            'city': null,
            'state': null,
            'zip': null,
        }
    
        if (ORDER_SHIPPING != 'False') {
            shippingInfo.address = form.address.value
            shippingInfo.city = form.city.value
            shippingInfo.state = form.state.value
            shippingInfo.zip = form.zip.value
        }
    
        if (user == 'AnonymousUser') {
            userFormData.fname = form.fname.value
            userFormData.email = form.email.value
        }
    
        // Make an AJAX request to your Django view
        $.ajax({
            url: "/process_order/",
            method: "POST",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify({'form':userFormData, 'shipping':shippingInfo}),
            success: function (response) {
                
                if (response['status'] == "success") {
    
                    var options = {
                            "key": "rzp_test_q03yAzvCR5hPJp",
                            "amount": response['amount'],
                            "currency": "INR",
                            "order_id": response['id'],
                            "name": "EComm",
                            "description": "Purchases",
                            "image": "http://127.0.0.1:8000/static/images/logo.png",
                            "handler": function(response) {
                                window.location.href = `/razorpay-success/?razorpay_order_id=${response.razorpay_order_id}`
                            },
                            "theme": {
                            "color": "#F37254"
                            }
                        };
                
                    var rzp1 = new Razorpay(options);
                    document.getElementById('rzp-button1').onclick = function(e) {
                    rzp1.open();
                    e.preventDefault();
                    }
    
                } else {
                    alert("Something went wrong. Please try again after some time...")
                    window.location.href = "/"
                }
    
            },
        });
    }
} catch (error) {
    console.log(error)
}


// Client-side validation using JavaScript
document.querySelector('#signupform').addEventListener('submit', function (event) {
    const password = document.querySelector('[name="password"]').value;
    const confirmPassword = document.querySelector('[name="confirm_password"]').value;

    if (password !== confirmPassword) {
        alert('Password and Confirm Password do not match.');
        event.preventDefault(); // Prevent form submission
    }
});