
let updateCart = document.querySelectorAll('.update-cart')
console.log("UpdateCart",updateCart);

for (i=0; i < updateCart.length; i++) {
  updateCart[i].addEventListener('click', function(){
    let productId = this.dataset.product
    let action = this.dataset.action
    console.log("PID", productId, "Action", action);
    
    console.log("USER", user)
    if(user == 'AnonymousUser') {
      console.log("User is not authenticated");
    } else {
      updateUserOrder(productId, action)
    }
  })
}

function updateUserOrder(productId, action) {
  console.log("User is authenticated, sending data...");
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