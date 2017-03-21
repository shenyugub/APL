$(function(){
	function zx(){
		if($('.head').outerHeight()+$('.content').outerHeight()+$('.footer').outerHeight()>document.documentElement.clientHeight ){

			$('.footer').css('position','static');
			$('.head').css({'position':'fixed','z-index':999});
			var h=$('.head').height();
			$('.content').css('margin-top',h+'px');
			
		}else{
			$('.footer').css('position','fixed');
			$('.head').css('position','static');
			$('.content').css('margin-top',0+'px');
		}
	}zx()
	$(window).on('resize',function(){
		if($('.head').outerHeight()+$('.content').outerHeight()+$('.footer').outerHeight()>document.documentElement.clientHeight ){
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
	$('.ul').on('click',function(){
		if($('.head').outerHeight()+$('.content').outerHeight()+$('.footer').outerHeight()>document.documentElement.clientHeight){
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