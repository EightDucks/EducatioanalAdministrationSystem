/**
 * Created by zhang on 2017/6/28.
 */
// $(function () {
//     alert('确定新建文件夹？')
// })
$(function(){

    var $parent = $('#divall'),$bgcolor = $('#divall li '),$carry = $('.carrynews'),
        $removenews = $('.remove'),$back = $('.back'),$removeright = $('#removethispc'),
        $namehide = $('#divall li input.changename'),$changename = $('#changename'),
        $uploadbutton=$('#uploadbutton'),$uploadfile=$('#exampleInputFile'),
		$mydownload=$('#downloadbutton');

    // $removenews.hide();
	// 下载
    $mydownload.click(function () {
        var txt='',courseid=$('.msgtransfer').attr("name"),filepath=$('.filepath').attr("name");
        $('input[type="checkbox"]:checked').each(
            function(){
                txt+=$(this).attr("name")+',';               
            })
        alert(txt);
        window.location.href='/EducationalSystem/resource/download/' + txt;
		
//        $.ajax({
//            url: '/EducationalSystem/resource/download/',
//            type: 'GET',
//            data: {down: txt,id:courseid, path:filepath},
//            success: function (response) {
//                window.location.href='/EducationalSystem/'
//                //console.log(response);
//            },
//        });
//		alert(txt);
    })
	
	//上传
	$uploadbutton.click(function () {
            //alert($uploadfile.attr("value"));
            var courseid=$('.msgtransfer').attr("name"),filepath=$('.filepath').attr("name");
			var form_data = new FormData();
            //var file_info = $('#exampleInputFile')[0].files[0]
            var length=$('#exampleInputFile')[0].files.length;
            for(var i=0;i<length;i++)
            {
                form_data.append('file',$('#exampleInputFile')[0].files[i]);
            }
            //form_data.append('file',file_info);
            form_data.append('path',filepath);
            form_data.append('courseid',courseid);
            //if(file_info==undefined)暂且不许要判断是否有附件
                //alert('你没有选择任何文件');
                //return false
            //}

            // 提交ajax的请求
            $.ajax({
                url:'/EducationalSystem/resource/upload/',
                type:'POST',
               // data: {file:form_data,courseid:id,path:filepath},
                data: form_data,
                processData: false,  // tell jquery not to process the data
                contentType: false, // tell jquery not to set contentType
                success: function(callback) {
					$('#divall').append(callback);
					//alert("上传成功");
					layer.msg("上传成功",{time: 1000 });
                }
            }); // end ajax
    })
    //新建

    $carry.click(function () {
            layer.prompt({title: '请输入文件夹名称', formType: 2}, function(pass, index){
                layer.close(index);
                if(typeof pass === 'string'){
                    // layer.msg(id)
                    var id = $('.msgtransfer').attr('name');
                    var filepath = $('.filepath').attr('name');
                    var name = pass
                    $.ajax({
                        url:'/EducationalSystem/resource/createFolder/',
                        type:'GET',
                        data:{courseid:id,path:filepath,foldername:name},
                        success:function (response) {
                                $('#divall').append(response)
                                // $('#divall').append(response)
                                layer.msg("创建成功",{time: 1000 });
                                /*绑定点击事件*/
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




                            }
                        }

                    );
                }
            });
    })

    //返回
    $back.live('click' , function(){
        setTimeout(
            function(){			
				/*$('#divall').html('<li class="myfolder"><input type="text" class="changename" name="1" value="{{res.name}}"disabled="disabled"/><input class="checkbox" name="{{res.3id}}" type="checkbox" value="" /></li>');
							    //为下次点击绑定事件
				 $('#divall li ').each(function () {
					$(this).dblclick(function () {
						alert("123");
						if($(this).hasClass('myfolder')){
							$('#divall').html('<li class="myfile"><input type="text" class="changename" name="1" value="{{res.name}}"disabled="disabled"/><input class="checkbox" name="{{res.3id}}" type="checkbox" value="" /></li>');

							}
						})
					})	*/
				var courseid=$('.msgtransfer').attr("name"),filepath=$('.filepath').attr("name");
				$.ajax({
                    url: '/EducationalSystem/resource/returnSuperiorMenu/',
                    type: "GET",
                    data: {id:courseid, path:filepath},
                    success: function (response) {
								if(response=='root')
								{
									//alert("已在根目录");
									layer.msg("已在根目录",{time: 1000 });
								}
								else
								{
									$('#divall').html(response);									
								}

							    //为下次点击绑定事件
								 $('#divall li ').each(function () {
									$(this).dblclick(function () {
										if($(this).hasClass('myfolder')){
											var txt=$(this).find('input[type="checkbox"]').attr("name"),foldername=$(this).find('input[type="text"]').attr("value"),filepath=$('.filepath').attr("name");
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
                    data: {id:courseid, path:filepath,flag:'2'},
                    success: function (response) {
                                //alert(response);
								$('.filepath').attr("name",response);
							},
                    }
                )
				//alter("返回结束")
				
            },250);
    }); 

    //复选框删除
    $bgcolor.live('click' , function(){
        var btns = document.getElementById('removebutton');
        //$removenews.fadeIn(250);
        $(this).addClass('bgclocrc');
        $(this).attr("id",'remove');
        
        btns.onclick = function(){//js 调用
            //alert('确定删除文件？');
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
								layer.msg("删除成功",{time: 1000 });
							},
							});
                        //$('.msgtransfer').val(txt);
                        //$removenews.fadeOut(250);
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



});