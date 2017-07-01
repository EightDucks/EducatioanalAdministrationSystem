/**
 * Created by zhang on 2017/6/28.
 */
// $(function () {
//     alert('确定新建文件夹？')
// })
$(function(){

    var $parent = $('#divall'),$bgcolor = $('#divall li '),$carry = $('.carrynews'),
        $removenews = $('.remove'),$back = $('.back'),$removeright = $('#removethispc'),
        $namehide = $('#divall li input.changename'),$changename = $('#changename');

    // $removenews.hide();

    //新建

    $carry.live('click' , function(){
        alert('确定新建文件夹？')
        setTimeout(
            function(){
                $parent.append("<li class='myfolder'><input type='text' class='changename'\ value='新建文件夹'/><input class='checkbox' type='checkbox' value='' /></li>");
				
			},250);
    });

    //返回
    $back.live('click' , function(){
        alert('确定返回？')
        setTimeout(
            function(){
				var id=$('.msgtransfer').attr("name"),filepath=$('.filepath').attr("name");
				$.ajax({
					url: '/EducationalSystem/resource/待填/',
					type: 'GET',
					data: {courseid:id, path:filepath},
					success: function (response) {
					alert('进入下一级');
					},
					});

            },250);
    }); //新文件夹不起作用！！

    //复选框删除
    $bgcolor.live('click' , function(){
        var btns = document.getElementById('removebutton');
        $removenews.fadeIn(250);
        $(this).addClass('bgclocrc');
        $(this).attr("id",'remove');
        
        btns.onclick = function(){//js 调用
            alert('确定删除文件夹？');
            setTimeout(
                function(){
						var txt='',courseid=$('.msgtransfer').attr("name"),filepath=$('.filepath').attr("name");
                        $('input[type="checkbox"]:checked').each(
						function(){
							txt+=$(this).attr("name")+',';
						$(this).parent().remove(); })
						txt+=courseid;
						//发起ajax删除请求
						$.ajax({
							url: '/EducationalSystem/resource/delete/',
							type: 'GET',
							data: {del: txt, path:filepath},
							success: function (response) {
								alert('删除成功');
							},
							});
                        $('.msgtransfer').val(txt);
                        $removenews.fadeOut(250);
                },250)
        }//
    });

    //增加双击事件
    $bgcolor.each(function () {
        $(this).dblclick(function () {
            if($(this).hasClass('myfolder')){
                var txt=$(this).find('input[type="checkbox"]').attr("name"),foldername=$(this).find('input[type="text"]').attr("value"),courseid=$('.msgtransfer').attr("name"),filepath=$('.filepath').attr("name");
				$.ajax({
                    url: '/EducationalSystem/resource/doubleclick/',
                    type: "GET",
                    data: {id:txt, name:foldername, path:filepath},
                    success: function (response) {
                                //alert(response);
                                $('#divall').html(response);
								//$('#divall').html('<li class="myfile"><input type="text" class="changename" name="1" value="{{res.name}}"disabled="disabled"/><input class="checkbox" name="{{res.3id}}" type="checkbox" value="" /></li>');
							    //为下次点击绑定事件
				 $('#divall li ').each(function () {
					$(this).dblclick(function () {
						if($(this).hasClass('myfolder')){
							var txt=$(this).find('input[type="checkbox"]').attr("name"),foldername=$(this).find('input[type="text"]').attr("value"),courseid=$('.msgtransfer').attr("name"),filepath=$('.filepath').attr("name");
							$.ajax({
								url: '/EducationalSystem/resource/doubleclick/',
								type: "GET",
								data: {id:txt, name:foldername, path:filepath},
								success: function (response) {
											//alert(response);
											$('#divall').html(response);

										},
								}
								)
							$.ajax({
								url: '/EducationalSystem/resource/returnVirpath/',
								type: "GET",
								data: {id:txt, name:foldername, path:filepath,flag:'1'},
								success: function (response) {
											//alert(response);
											$('.filepath').attr("name",response);

										},
								}
							)
						}
					})
				})
				//
							},
                    }
				)
				$.ajax({
                    url: '/EducationalSystem/resource/returnVirpath/',
                    type: "GET",
                    data: {id:txt, name:foldername, path:filepath,flag:'1'},
                    success: function (response) {
                                //alert(response);
								$('.filepath').attr("name",response);
							},
                    }
                )

            }
        })
    })

    //修改文件名
    $namehide.live('focus' , function(){
        $(this).css('border','1px solid #FF0000');
        $(this).val('');
        //键盘控制
        /* document.onkeydown = function (event) {
         var e=event.srcElement;
         if(event.keyCode==13)
         {
         alert('确定修改文件名?');
         return true;
         }
         }*/
    });
    $namehide.live('blur' , function(){
        alert('确定修改文件名？')
        $(this).css('border','none');
        if( $(this).val() == ""){
            $(this).val('新建文件夹');
        }else{
            // $(this).parent().find('span').text() = $(this).value;
        }
    });

    //纯属娱乐耍耍，如需更多功能亲们自行开发...............


});