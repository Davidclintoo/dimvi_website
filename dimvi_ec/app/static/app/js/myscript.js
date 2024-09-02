


$('.plus_cart').click(function(){
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2];
    console.log('pid', id);
    $.ajax({
        type: "GET",
        url: "/plus_cart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("data", data);
            eml.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('total_amount').innerText = data.total_amount;
        }
    });
});


$('.minus_cart').click(function(){
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2];
    console.log('pid', id);
    $.ajax({
        type: "GET",
        url: "/minus_cart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("data", data);
            eml.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('total_amount').innerText = data.total_amount;
        }
    });
});


$('.remove').click(function(){
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2];
    console.log('pid', id);
    $.ajax({
        type: "GET",
        url: "/remove",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("data", data);
            eml.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('total_amount').innerText = data.total_amount;
        }
    });
});

