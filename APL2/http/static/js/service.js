$(function(){
	$(window).on('load',function(){
		if($('.head').height()+$('.content').height()+10>$(window).height()){
			$('.head').css({'position':'fixed','z-index':999});
			var h=$('.head').height();
			$('.content').css('margin-top',h+'px');
			
		}else{
			$('.head').css('position','static');
			$('.content').css('margin-top',0+'px');
		}
	})
	$(window).on('resize',function(){
		if($('.head').height()+$('.content').height()+10>$(window).height()){
			$('.head').css({'position':'fixed','z-index':999});
			var h=$('.head').height();
			$('.content').css('margin-top',h+'px');
			
		}else{
			$('.head').css('position','static');
			$('.content').css('margin-top',0+'px');
		}
	})
	
})