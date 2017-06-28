/**
 * Created by zhang on 2017/6/28.
 */
// $(function () {
//     alert('确定新建文件夹？')
// })
$(function(){
    var $parent = $('#divall'),$bgcolor = $('#divall li'),$carry = $('.carrynews'),
        $removenews = $('.remove'),$removeall = $('.removeall'),$removeright = $('#removethispc'),
        $namehide = $('#divall li input.changename'),$changename = $('#changename');
    $removenews.hide();

    //新建

    $carry.live('click' , function(){
        alert('确定新建文件夹？')
        setTimeout(

            function(){
                $parent.append("<li><input type='text' class='changename'\ value='新建文件夹'/><input class='checkbox' type='checkbox' value='' /></li>");
            },500);
    });

    //清空
    $removeall.live('click' , function(){
        alert('确定清空所有文件夹？')
        setTimeout(
            function(){
                $parent.empty();

            },500);
    }); //新文件夹不起作用！！

    //变色
    $bgcolor.live('click' , function(){
        var btns = document.getElementById('removebutton');
        btns02 = document.getElementById('removethispc');
        $removenews.fadeIn(250);
        $(this).addClass('bgclocrc');
        $(this).attr("id",'remove').siblings().attr('id','');
        $( " input[type=text] ").attr("id",'namecc').siblings().attr('id',' ');
        btns.onclick = function(){//js 调用
            alert('确定删除文件夹？');
            setTimeout(
                function(){
                    if($bgcolor.hasClass('bgclocrc'))
                    {
                        $('input[type="checkbox"]:checked').each(function(){
						$(this).parent().remove(); })
                        
                        $removenews.fadeOut(250);
                    }else
                    {
                        alert('请选择文件')
                    }
                },250)
        }//

        

        //右键菜单
        var container = document.getElementById('remove');
        var menu = document.getElementById('menu');

        /*显示菜单*/
        function showMenu() {

            var evt = window.event || arguments[0];

            /*获取当前鼠标右键按下后的位置，据此定义菜单显示的位置*/
            var rightedge = container.clientWidth-evt.clientX;
            var bottomedge = container.clientHeight-evt.clientY;

            /*如果从鼠标位置到容器右边的空间小于菜单的宽度，就定位菜单的左坐标（Left）为当前鼠标位置向左一个菜单宽度*/
            if (rightedge < menu.offsetWidth)
                menu.style.left = container.scrollLeft + evt.clientX - menu.offsetWidth + "px";
            else
            /*否则，就定位菜单的左坐标为当前鼠标位置*/
                menu.style.left = container.scrollLeft + evt.clientX + "px";

            /*如果从鼠标位置到容器下边的空间小于菜单的高度，就定位菜单的上坐标（Top）为当前鼠标位置向上一个菜单高度*/
            if (bottomedge < menu.offsetHeight)
                menu.style.top = container.scrollTop + evt.clientY - menu.offsetHeight + "px";
            else
            /*否则，就定位菜单的上坐标为当前鼠标位置*/
                menu.style.top = container.scrollTop + evt.clientY + "px";

            /*设置菜单可见*/
            menu.style.display = "block";
            LTEvent.addListener(menu,"contextmenu",LTEvent.cancelBubble);
        }
        /*隐藏菜单*/
        function hideMenu() {
            menu.style.display = 'none';
        }
        LTEvent.addListener(container,"contextmenu",LTEvent.cancelBubble);
        LTEvent.addListener(container,"contextmenu",showMenu);
        LTEvent.addListener(document,"click",hideMenu);

        //
        $changename.live('click' , function(){

            if($bgcolor.hasClass('bgclocrc'))
            {
                $('#remove').find('.changename').val('');
                $('#remove').find('.changename').css('border','1px solid #FF0000')
            }else
            {
                alert('请选择文件')
            }

        });

    });

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