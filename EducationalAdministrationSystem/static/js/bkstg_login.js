function login() {
    var password = hex_sha1($("#password").val());
    
    $.ajax({
            url: "../php/login.php",
            type: "POST",
            data: {
                "action": "bkstg_login",
                "password": password
            },
            dataType: "json"
    }).done(function(data) {
        if(data['status'] == 0) {
            
                window.location="index.php";
        } else {

            $(".alert").fadeIn();
        }
    });
    return false;
}