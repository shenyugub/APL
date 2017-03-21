$(function(){
	//渲染数据
	$.ajax({
		url:'',
		type:'get',
		success:function(e){
			console.log(e)
		},
		error:function(){
			alert("失败");
		}
	})
	//card效果
	$('.card').on('mouseover',function(){
		$(this).css({'left':'-5px','top':'-5px'});
		$(this).css('box-shadow','2px 2px 2px #ccc');
	})
	$('.card').on('mouseout',function(){
		$(this).css({'left':'0px','top':'0px'});
		$(this).css('box-shadow','2px 2px 2px transparent');
	})
	/*$('.pro').on('mouseover',function(){
		$(this).css({'left':'-5px','top':'-5px'});
		$(this).css('box-shadow','2px 2px 2px #ccc');
	})
	$('.pro').on('mouseout',function(){
		$(this).css({'left':'0px','top':'0px'});
		$(this).css('box-shadow','2px 2px 2px transparent');
	})*/
	$('.card').on('click',function(){
		location.href="./bp_manage.html";
	})
})