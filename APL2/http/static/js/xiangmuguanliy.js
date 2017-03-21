$(function(){
	$('.tab').find('span').eq(0).css('border-bottom','1px solid #2aabd2');
	$('.tab').find('span').on('click',function(){
		$(this).css('border-bottom','1px solid #2aabd2').siblings().css('border-bottom','1px solid transparent')
	})
	$('.xmlist').on('mouseover',function(){
		$(this).css({'left':'-5px','top':'-5px'});
		$(this).css('box-shadow','2px 2px 2px #ccc');
	})
	$('.xmlist').on('mouseout',function(){
		$(this).css({'left':'0px','top':'0px'});
		$(this).css('box-shadow','2px 2px 2px transparent');
	})
	$('.xmlist').on('click',function(){
		var ids=$(this).attr('id');
		location.href="/startup/projects/"+ids+"";
	})
})