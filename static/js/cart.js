const updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    const element = updateBtns[i];
    element.addEventListener('click', function(){
        const productId = this.dataset.product
        const action = this.dataset.action
        if(user === "AnonymousUser"){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action){
    console.log('Add cookie')    
    if(action === "add"){
        if(!cart[productId]){
            cart[productId] = {'quantity': 1}
            console.log(cart);
        }else{
            cart[productId]['quantity']+=1
            console.log(cart);
        }
    }

    if(action === "remove"){
        cart[productId]['quantity']--

        if(cart[productId]['productId'] <= 0){
            console.log('Item was deleted');
            delete cart[productId]
        }
    }

    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId, action){
    console.log('Sending data...');
    const url = '/update_item/'
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({"productId": productId, 'action': action, "csrftoken": csrftoken}),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        }
    }).then((res) => res.json()).then((data) => {
        location.reload()
    })
}