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
		$('#tck').css('marginTop',-h+'px')
	})
	$('#close').on('click',function(){
		$('.mark').hide();
		$('#tck').hide();
	})
	$('#dpBtn').on('click',function(){
		var con=$('#textarea').val();
		alert(con);
	})
})