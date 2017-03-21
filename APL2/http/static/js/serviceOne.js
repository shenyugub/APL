$(function(){
	$('.xr').on('click',function(){
		location.href="./service_category.html";
	})
	$('#custom').on('click',function(){
		location.href="./service_custom.html";
	})
	$('#sea').on('click',function(){
		var texts=$('#texts').val();
		alert(texts);
	})
	$('.xq').on('mouseover',function(){
		$(this).css({'left':'-5px','top':'-5px'});
		$(this).css('box-shadow','2px 2px 2px #ccc');
	})
	$('.xq').on('mouseout',function(){
		$(this).css({'left':'0px','top':'0px'});
		$(this).css('box-shadow','2px 2px 2px transparent');
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