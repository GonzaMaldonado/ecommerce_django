
let updateCart = document.querySelectorAll('.update-cart')

for (i=0; i < updateCart.length; i++) {
  updateCart[i].addEventListener('click', function(){
    let productId = this.dataset.product
    let action = this.dataset.action
    
    if(user == 'AnonymousUser') {
      addCookieItem(productId, action)
    } else {
      updateUserOrder(productId, action)
    }
  })
}

function addCookieItem(productId, action) {
  console.log("User is not authenticated");

  if (action == 'add') {
    if (cart[productId] == undefined) {
      cart[productId] = {'quantity': 1}
    } else {
      cart[productId]['quantity'] += 1
    }
  }

  if (action == 'remove') {
    cart[productId]['quantity'] -=1

    if (cart[productId]['quantity'] <= 0) {
      console.log('Item should be deleted')
      delete cart[productId]
    }
  }

  console.log('Cart:', cart);
  document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
  location.reload()
}

function updateUserOrder(productId, action) {
  let url = '/update_item/'
  fetch(url,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({'productId': productId, 'action': action})
    }
  )
  .then((response) => {
    return response.json()
  })
  .then((data) => {
    console.log("Data received from server", data);
    location.reload()
  })
}