
$(document).ready(function(){
	$("#course_confirm").hide();
  $("#course_rewrite").click(function(){
   // $(this).css("background-color","#cccccc");
   $("#semester_name").removeAttr("disabled");
   $("#course_name").removeAttr("disabled");
   $("#course_time").removeAttr("disabled");
   $("#course_teacher").removeAttr("disabled");
   $("#course_location").removeAttr("disabled");
   $("#course_point").removeAttr("disabled");
   $("#course_timelength").removeAttr("disabled");
	$("#course_confirm").show();
	$("#course_rewrite").hide();
  });
  $("#course_confirm").click(function(){
   $("#semester_name").attr("disabled","disabled");
   $("#course_name").attr("disabled","disabled");
   $("#course_time").attr("disabled","disabled");
   $("#course_teacher").attr("disabled","disabled");
   $("#course_location").attr("disabled","disabled");
   $("#course_point").attr("disabled","disabled");
   $("#course_timelength").attr("disabled","disabled");
	$("#course_rewrite").show();
	$("#course_confirm").hide();
  });
  
});