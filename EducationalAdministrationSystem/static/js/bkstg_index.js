function logout(){
    $.ajax({
        type: "POST",
        url: '../php/login.php',
        dataType: 'json',
        data: {
            action: "logout"
        },
        success: function(data) {
            if(data['status']==0){
                window.location="login.php";
            }
            else {
                alert(data['msg']);
            }
        }
    });
}

$(document).ready(function() {
        
    $("#renew").click(function(){
        var old = hex_sha1($("#modal-body").find(".old-psw").val());
        var new1 = hex_sha1($("#modal-body").find(".new-psw1").val());
        var new2 = hex_sha1($("#modal-body").find(".new-psw2").val());

        if(new1=="") {
            $('<div id="alertx" class="row"><div class="col-md-10 col-md-offset-1"><div class="alert alert-danger" role="alert"><p>请设置密码！</p></div></div></div>').insertBefore($("this")).fadeIn();
            setTimeout(function(){
                $('#alertx').fadeOut();
            },2000);
        } else if(new1!=new2) {
            $('<div id="alertx" class="row"><div class="col-md-10 col-md-offset-1"><div class="alert alert-danger" role="alert"><p>两次密码不一致！</p></div></div></div>').insertBefore($("this")).fadeIn();
            setTimeout(function(){
                $('#alertx').fadeOut();
            },2000);
        }
        else{
            $.ajax({
                    url: "../php/bkstg.php",
                    type: "POST",
                    data: {
                        "action" : "reset_psw",
                        "old" : old,
                        "new" : new1
                    },
                    dataType: "json"
            }).done(function(data) {
                switch (data["status"]) {
                    case 0: //success
                        alert("修改成功！");
                        window.location.reload(true);
                        break;
                    case -1: //error
                        alert(data["msg"]);
                        break;
                    default:
                        break;
                }
            });
        }
    });

});