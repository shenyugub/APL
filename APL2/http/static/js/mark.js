$(function(){
	var t=$('.head').height();
	$('#all').css('top',t);
	$('#emailId').on('click',function(e){
var event=e || window.event;
		event.stopPropagation();
		$('#all').toggle();
	})
	$(document).on('click',function(e){
		var tar=$('#all');
		var event=e || window.event;
		if(!tar.is(event.target) && tar.has(event.target).length === 0){
			$('#all').hide();
		}
	})
})