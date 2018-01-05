$(document).ready(function(){
    var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val()
    var customer_req = false
//    var customer_check_url = $('input[name="customer_check_url"]').val()

    //    check for existing email address
//    $('#email_address').on("change keyup paste", function(){
//        var email = $(this).val();
//        if (customer_req) {
//            customer_req.abort()
//        }
//        customer_req = $.post(customer_check_url, {
//            'csrfmiddlewaretoken': csrfmiddlewaretoken,
//            'email': email
//        }, function(data) {
//            console.log(data);
//        })
//    })
})
