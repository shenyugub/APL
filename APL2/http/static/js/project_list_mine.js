$(function(){
	$('.xmlist').on('click',function(){
        var ids = $(this).attr('id');
		location.href="/investor/projects_mine_detail/" + ids + "";
	})
	$('.xmlist').on('mouseover',function(){
		$(this).css({'left':'-5px','top':'-5px'});
		$(this).css('box-shadow','2px 2px 2px #ccc');
	})
	$('.xmlist').on('mouseout',function(){
		$(this).css({'left':'0px','top':'0px'});
		$(this).css('box-shadow','2px 2px 2px transparent');
	})
})