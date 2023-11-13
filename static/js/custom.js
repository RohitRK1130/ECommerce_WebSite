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
