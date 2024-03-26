// $('#slider1, #slider2, #slider3').owlCarousel({
//     loop: true,
//     margin: 20,
//     responsiveClass: true,
//     responsive: {
//         0: {
//             items: 2,
//             nav: false,
//             autoplay: true,
//         },
//         600: {
//             items: 4,
//             nav: true,
//             autoplay: true,
//         },
//         1000: {
//             items: 6,
//             nav: true,
//             loop: true,
//             autoplay: true,
//         }
//     }
// })

// $(document).ready(function(){
//     $('#add-to-cart-form').on('submit', function(e){
//         e.preventDefault();
//         var form = $(this);
//         var url = form.attr('data-url');
//         $.ajax({
//             type: 'POST',
//             url: url,
//             data: form.serialize(),
//             dataType: 'json',
//             success: function(data){
//                 if (data.status === 'success') {
//                     alert('Item added to cart successfully');
//                     // Optionally, update the cart count or show a success message
//                 } else {
//                     alert('Error: ' + data.message);
//                 }
//             },
//             error: function(xhr, textStatus, errorThrown){
//                 alert('Error: ' + xhr.responseText);
//             }
//         });
//     });
// });

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    console.log('pid=',id)
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log('data=',data)
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    console.log('pid=',id)
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log('data=',data)
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})


$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove() 
        }
    })
})

function darkmode() {
    const element = document.body;
    element.classList.toggle("dark-mode");
 }

 $(document).ready(function() {
    $("#wishlist-form").submit(function(event) {
        event.preventDefault(); // Prevent default form submission

        var productId = $(this).data("product-id");
        var formData = $(this).serialize(); // Serialize form data

        $.ajax({
            url: "{% url 'add_to_wishlist' %}",
            type: "POST",
            data: formData,
            dataType: "json",
            success: function(data) {
                // Handle success response
                console.log(data);
                // Update button icon based on response
                var button = $("#wishlist-form button");
                if (data.success) {
                    button.html('<span class="material-symbols-outlined">favorite</span>');
                } else {
                    button.html('<span class="material-symbols-outlined">heart_broken</span>');
                }
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.error("Error:", error);
            }
        });
    });
});
