$(function(){
	$('.xmlist').on('click',function(){
        var ids = $(this).attr('id');
        location.href = "/startup/investors/" + ids + "";
	})
	$('#search').on('click',function(){
		var txt=$('#txt').val();
		alert(txt);
	})
	$('.allChoose').css('background','#5bc0de');
	//头部的点击变背景效果
	$('.fl').find('div').on('click',function(){
		$(this).css('background','#5bc0de').siblings().css('background','');
		$(this).parent().prev().css('background','')
	})
	$('.allChoose').on('click',function(){
		$(this).css('background','#5bc0de');
		$(this).next().find('div').css('background','');
	})
})