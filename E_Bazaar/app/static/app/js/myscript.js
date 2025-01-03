$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 3,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        },
        1500: {
            items: 7,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


$('.plus-cart').click(function () {
    // console.log("Plus Clicked")
    let id = $(this).attr("pid").toString();
    let elm = this.parentNode.children[2];
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id:id
        },
        success: function (data) {
            // console.log(data)
            // console.log("Success")
            elm.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

$('.minus-cart').click(function () {
    // console.log("Plus Clicked")
    let id = $(this).attr("pid").toString();
    let elm = this.parentNode.children[2];
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id:id
        },
        success: function (data) {
            // console.log(data)
            // console.log("Success")
            elm.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

$('.remove-cart').click(function () {
    // console.log("Plus Clicked")
    let id = $(this).attr("pid").toString();
    let elm = this;
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id:id
        },
        success: function (data) {
            // console.log(data)
            // console.log("Success")
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            elm.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})



$('.plus-wishlist').click(function(){
    let id = $(this).attr("pid").toString();
    console.log("plus : ",id)

    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})


$('.minus-wishlist').click(function(){
    let id = $(this).attr("pid").toString();
    console.log("minus : ",id)

    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})




// this code is work only 1 order cancle 
// $('.btn-primary').click(function () {
//     let orderId = $(this).attr("data-order-id").toString(); // Pass the order ID dynamically
//     console.log(orderId);
//     $.ajax({
//         type: 'POST',
//         url: '/cancel_order/',
//         data: {
//             order_id: orderId,
//             csrfmiddlewaretoken: '{{ csrf_token }}' // Include CSRF token
//         },
//         success: function (response) {
//             alert('Order cancelled successfully!');
//             location.reload();
//         },
//         error: function (error) {
//             alert('Something went wrong!');
//             console.error(error.responseText);
//         }
//     });
// });




// this code work for multiple order cancle but it conflicts when same user can can cancle the same product item 

$(document).ready(function () {
    // Set the correct order ID when the cancel button is clicked
    $('.order-cancel-btn').click(function () {
        let orderId = $(this).data('order-id'); // Get the product ID
        console.log("Order ID to cancel: ", orderId);
        $('#exampleModal .confirm-cancel-btn').data('order-id', orderId); // Set it for the confirm button
    });

    // Handle the Confirm button click
    $('.confirm-cancel-btn').click(function () {
        let orderId = $(this).data('order-id'); // Get the product ID from the confirm button
        console.log("Order ID to cancel: ", orderId);

        $.ajax({
            type: 'POST',
            url: '/cancel_order/',
            data: {
                order_id: orderId,
                csrfmiddlewaretoken: '{{ csrf_token }}' // Include CSRF token
            },
            success: function (response) {
                alert('Order cancelled successfully!');
                location.reload(); // Reload the page to reflect changes
            },
            error: function (error) {
                alert('Something went wrong!');
                console.error(error.responseText);
            }
        });

        // Hide the modal after confirming
        $('#exampleModal').modal('hide');
    });
});




// Select all radio buttons and the container for the "Continue" button
const addressRadios = document.querySelectorAll('.address-radio');
const continueButtonContainer = document.getElementById('continue-btn-container');

// Add event listeners to each radio button
addressRadios.forEach((radio) => {
    radio.addEventListener('change', () => {
        // Display the "Continue" button container when a radio button is selected
        continueButtonContainer.style.display = 'block';
    });
});





// document.querySelectorAll('.order-cancel-btn').forEach(button => {
//     button.addEventListener('click', function() {
//         const orderId = this.getAttribute('data-order-id'); // Fetch the order ID
//         console.log("Order ID:", orderId); // For debugging

//         // Pass this ID to your modal or AJAX call
//         document.getElementById('hidden-order-id').value = orderId;
//     });
// });


// document.getElementById('confirm-cancel').addEventListener('click', function() {
//     const orderId = document.getElementById('hidden-order-id').value;
//     console.log("Order ID:", orderId); // For debugging

//     // Send the order ID to your backend via AJAX
//     fetch('/cancel_order', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': '{{ csrf_token }}' // Include CSRF token for security
//         },
//         body: JSON.stringify({ order_id: orderId })
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log(data.message); // Debug response
//         if (data.success) {
//             alert('Order cancelled successfully!');
//             location.reload(); // Reload the page or update UI
//         } else {
//             alert('Failed to cancel order.');
//         }
//     })
//     .catch(error => console.error('Error:', error));
// });












// $('.remove-cart').click(function () {
//     let id = $(this).attr("pid").toString();
//     let elm = this;

//     $.ajax({
//         type: "GET",
//         url: "/removecart",
//         data: {
//             prod_id: id
//         },
//         success: function (data) {
//             let amountElement = document.getElementById("amount");
//             let totalAmountElement = document.getElementById("totalamount");
//             let shippingElement = document.getElementById("shippingcharge");

//             // Update the amount and total amount
//             amountElement.innerText = data.amount;

//             if (data.amount < 500) {
//                 let shippingCharge = 40.00;
//                 shippingElement.innerText = shippingCharge;
//             }
//             else{
//                 let value = 'FREE';
//                 shippingElement.innerText = value;


//             }

//             // Check if the amount is less than 500
//             if(data.amount == 0) {
//                 totalAmountElement.innerText = data.amount + 0;
//             }
//             else if (data.amount < 500) {
//                 let shippingCharge = 40;
//                 totalAmountElement.innerText = data.amount + shippingCharge;
//                 // document.getElementById("shippingcharge").innerText = `Shipping Charge: ₹${shippingCharge}`;
//             } else {
//                 totalAmountElement.innerText = data.amount;
//                 // document.getElementById("shippingcharge").innerText = `Shipping Charge: ₹0`;
//             }

//             // Remove the cart item
//             elm.parentNode.parentNode.parentNode.parentNode.remove();
//         }
//     });
// });


// $('.remove-cart').click(function () {
//     let id = $(this).attr("pid").toString();
//     let elm = this;

//     $.ajax({
//         type: "GET",
//         url: "/removecart",
//         data: {
//             prod_id: id
//         },
//         success: function (data) {
//             let amountElement = document.getElementById("amount");
//             let totalAmountElement = document.getElementById("totalamount");
//             let shippingChargeElement = document.getElementById("shippingcharge");

//             // Update the amount
//             amountElement.innerText = data.amount;

//             // Check conditions for shipping charges
//             if (data.amount === 0) {
//                 // Free shipping when amount is 0
//                 shippingChargeElement.innerText = "0";
//                 totalAmountElement.innerText = "0";
//             } else if (data.amount < 500) {
//                 // Add shipping charge for amounts less than 500
//                 let shippingCharge = 40;
//                 shippingChargeElement.innerText = `Shipping: ₹${shippingCharge}`;
//                 totalAmountElement.innerText = data.amount + shippingCharge;
//             } else {
//                 // Free shipping for amounts 500 and above
//                 shippingChargeElement.innerText = "Shipping: FREE";
//                 totalAmountElement.innerText = data.amount;
//             }

//             // Remove the cart item from the DOM
//             elm.parentNode.parentNode.parentNode.parentNode.remove();
//         }
//     });
// });


// $('.remove-cart').click(function () {
//     let id = $(this).attr("pid").toString();
//     let elm = this;

//     $.ajax({
//         type: "GET",
//         url: "/removecart",
//         data: {
//             prod_id: id
//         },
//         success: function (data) {
//             // Select DOM elements for amount, total amount, and shipping charge
//             let amountElement = document.getElementById("amount");
//             let totalAmountElement = document.getElementById("totalamount");
//             let shippingChargeElement = document.getElementById("shippingcharge");

//             // Update the amount dynamically
//             let amount = data.amount; // The updated cart amount from the server
//             amountElement.innerText = amount;

//             // Shipping charge logic
//             if (amount === 0 || amount === "0") {
//                 // Case 1: Cart is empty
//                 shippingChargeElement.innerText = "Shipping: FREE";
//                 totalAmountElement.innerText = "0";
//             } else if (amount < 500) {
//                 // Case 2: Amount is less than 500
//                 let shippingCharge = 40;
//                 shippingChargeElement.innerText = `Shipping: ₹${shippingCharge}`;
//                 totalAmountElement.innerText = parseFloat(amount) + shippingCharge;
//             } else {
//                 // Case 3: Amount is 500 or more
//                 shippingChargeElement.innerText = "Shipping: FREE";
//                 totalAmountElement.innerText = amount;
//             }

//             // Remove the cart item from the DOM
//             elm.parentNode.parentNode.parentNode.parentNode.remove();
//         },
//         error: function (xhr, status, error) {
//             console.error("AJAX Error:", status, error);
//             alert("Something went wrong! Please try again.");
//         }
//     });
// });

