
$('#teacherid_attachment_add').click(function(){
    var i = $('.shiyi_teacherid').length;
    var head = "<div class=\"form-group shiyi_teacherid\" id=\"teacherid_"
    var mid="\"><label class=\"col-sm-2 control-label\"></label><div class=\"col-sm-3\"><input type=\"text\" class=\"form-control\" name=\"course_teacherid_"
    var tail = "\"required/></div></div>"
    var content = head;
    content += i;
    content += mid;
    content += i;
    content += tail;
    $('#multi-teacherid-holder').before(content);
    if($('.shiyi_teacherid').length > 1){
        $('#teacherid_attachment_rm').removeClass('shiyi_hide');
    }
})

$('#teacherid_attachment_rm').click(function() {
    var i = $('.shiyi_teacherid').length - 1;
    var name = "#teacherid_";
    name = name + i;
    $(name).remove();
    if($('.shiyi_teacherid').length <= 1){
        $('#teacherid_attachment_rm').addClass('shiyi_hide');
    }
})