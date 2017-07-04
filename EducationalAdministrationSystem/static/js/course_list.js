/*
 * Magry 2017/7/4
 */
var cnt = $('#course_cnt').val();
var ps = Math.ceil(cnt/6);
var page = $('#course_page').val();
$(document).ready(function(){
  //显示当前页2行课程内容
  $('.course_row').addClass('magry_hide');
  var show_r1=(page-1)*2;
  var show_r2=show_r1+1;
  var s1="#course_row_"+show_r1;
  var s2="#course_row_"+show_r2;
  $(s1).removeClass('magry_hide');
  $(s2).removeClass('magry_hide');
  //显示页码
  var i = 0;
  while (i<ps) {
    i+=1;
    str="<li class=\"course_page_page\" id=\"course_page_"+i+"\" value=\""+i+"\"><a>"+i+"</a></li>";
    $('#course_page_next').before(str);
  }
  $(".course_page_page").click(function () {
    page = Number($(this).val());
    $('#course_page').attr("value",page);
    $('.course_row').addClass('magry_hide');
    var show_r1=(page-1)*2;
    var show_r2=show_r1+1;
    var s1="#course_row_"+show_r1;
    var s2="#course_row_"+show_r2;
    $(s1).removeClass('magry_hide');
    $(s2).removeClass('magry_hide');
  })
})
$('#course_page_previous').click(function () {
  page = Number($('#course_page').val());
  if(page>1){
    page=page-1;
    $('#course_page').attr("value",page);
    $('.course_row').addClass('magry_hide');
    var show_r1=(page-1)*2;
    var show_r2=show_r1+1;
    var s1="#course_row_"+show_r1;
    var s2="#course_row_"+show_r2;
    $(s1).removeClass('magry_hide');
    $(s2).removeClass('magry_hide');
  }
})
$('#course_page_next').click(function () {
  page = Number($('#course_page').val());
  if(page<ps){
    page++;
    $('#course_page').attr("value",page);
    $('.course_row').addClass('magry_hide');
    var show_r1=(page-1)*2;
    var show_r2=show_r1+1;
    var s1="#course_row_"+show_r1;
    var s2="#course_row_"+show_r2;
    $(s1).removeClass('magry_hide');
    $(s2).removeClass('magry_hide');
  }
})
