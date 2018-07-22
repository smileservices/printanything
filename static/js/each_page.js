$(document).ready(function(){
    console.log(hideTopCart);
    if (Boolean(hideTopCart) !== true) {
         cart.refresh();
    }
})
