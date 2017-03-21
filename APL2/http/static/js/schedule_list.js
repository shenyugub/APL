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
	$('.dp').on('click',function(){
		$('.mark').show();
		$('#tck').show();
		var h=$('#tck').height()/2;
		$('#tck').css('marginTop',-h+'px');
		$('body').css('overflow','hidden');

	})
	$('#close').on('click',function(){
		$('.mark').hide();
		$('#tck').hide();
		$('body').css('overflow','auto');
	})
	$('#dpBtn').on('click',function(){
		alert($('#txt').val())
	})
})