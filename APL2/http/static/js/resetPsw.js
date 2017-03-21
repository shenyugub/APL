$(function(){
	$('#qrBtn').on('click',function(){
		var newPaw=$('#newPaw').val(),
		    newPaw1=$('#newPaw1').val();
		console.log(newPaw+"_"+newPaw1);
		if(newPaw!=newPaw1){
			$('#ts').css('display','block');
		}else{
			$('#ts').css('display','none');
		}
	})
})