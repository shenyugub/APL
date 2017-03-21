$(function(){
	$('.bz').on('click',function(){
		$('.mark').show();
		$('#tck').show();
	})
	$('#tj').on('click',function(){
		var lyTxt=$('#lyTxt').val();
		alert(lyTxt);
	})
})