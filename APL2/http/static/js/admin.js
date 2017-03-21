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
	$('.ul').find('li').on('click',function(){
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
	$('.cancel').on('click',function(){
		$('.mark').hide();
		$('#tck').hide();
		$('body').css('overflow','auto');
	})
})