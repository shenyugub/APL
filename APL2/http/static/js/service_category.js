$(function(){
	$(window).on('load',function(){
		if($('.container-fluid').height()>$(window).height()){
			var w=$('.container-fluid').width();
			var h=$('.container-fluid').height();
			$('.mark').width(w);
			$('.mark').height(h);
		}else{
			var w=$(window).width();
			var h=$(window).height();
			$('.mark').width(w);
			$('.mark').height(h);
		}
	})
	$(window).on('resize',function(){
		if($('.container-fluid').height()>$(window).height()){
			var w=$('.container-fluid').width();
			var h=$('.container-fluid').height();
			$('.mark').width(w);
			$('.mark').height(h);
		}else{
			var w=$(window).width();
			var h=$(window).height();
			$('.mark').width(w);
			$('.mark').height(h);
		}
	})
	$('.sc').on('click',function(){
		$('.mark').show();
		$('#tck').show();
		var h=$('#tck').height()/2;
		$('#tck').css('marginTop',-h+'px');
		$('#tck').find('input').val("");
	})
	$('#xd').on('click',function(){
		$('.mark').show();
		$('#tck').show();
		var h=$('#tck').height()/2;
		$('#tck').css('marginTop',-h+'px');
		$('#tck').find('input').val("");
	})
	$('#close').on('click',function(){
		$('.mark').hide();
		$('#tck').hide();
	})
	$('.topBtn').on('mouseover',function(){
		$(this).css({'left':'-5px','top':'-5px'});
		$(this).css('box-shadow','2px 2px 2px #ccc');
	})
	$('.topBtn').on('mouseout',function(){
		$(this).css({'left':'0px','top':'0px'});
		$(this).css('box-shadow','2px 2px 2px transparent');
	})
})