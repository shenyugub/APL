$(function(){
	$(window).on('load',function(){
		if($('.head').height()+$('.content').height()+$('.content1').height()+$('.footer').height()>$(window).height()){
			$('.footer').css('position','static');
			$('.head').css({'position':'fixed','z-index':999});
			var h=$('.head').height();
			$('.content').css('margin-top',h+'px');
			
		}else{
			$('.footer').css('position','fixed');
			$('.head').css('position','static');
			$('.content').css('margin-top',0+'px');
		}
	})
	$(window).on('resize',function(){
		if($('.head').height()+$('.content').height()+$('.content1').height()+$('.footer').height()>$(window).height()){
			$('.footer').css('position','static');
			$('.head').css({'position':'fixed','z-index':999});
			var h=$('.head').height();
			$('.content').css('margin-top',h+'px');
			
		}else{
			$('.footer').css('position','fixed');
			$('.head').css('position','static');
			$('.content').css('margin-top',0+'px');
		}
	})
})