//Magry Jul. 1 2017
$('#btn_refuse_team').click(function () {
  if($('#refuse_reason').hasClass('magry_hide')){
    $('#refuse_reason').removeClass('magry_hide');
    $('#btn_approve_team').addClass('disabled');
    $('#btn_refuse_team').addClass('disabled');
    $('#btn_refuse_team_hide').removeClass('magry_hide');
  }
})
$('#btn_refuse_team_hide').click(function () {
  if($('#refuse_reason').hasClass('magry_hide')==false){
    $('#refuse_reason').addClass('magry_hide');
    $('#btn_approve_team').removeClass('disabled');
    $('#btn_refuse_team').removeClass('disabled');
    $('#btn_refuse_team_hide').addClass('magry_hide');
  }
})
$('#btn_adj_team').click(function(){
  if($('#adj_team').hasClass('magry_hide')){
    $('#adj_team').removeClass('magry_hide');
    $('#btn_adj_team').addClass('disabled');
    $('#btn_adj_team_hide').removeClass('magry_hide');
  }
})
$('#btn_adj_team_hide').click(function(){
  if($('#adj_team').hasClass('magry_hide')==false){
    $('#adj_team').addClass('magry_hide');
    $('#btn_adj_team').removeClass('disabled');
    $('#btn_adj_team_hide').addClass('magry_hide');
  }
})
