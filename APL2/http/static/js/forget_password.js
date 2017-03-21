$(function(){
	var timer=null,num=60;
	$('#hqyzm').on('click',function(){
		$(this).attr('disabled',true);
		$(this).css('color','#999');
		timer=setInterval(function(){
			$('#hqyzm').text('发送('+num+')');
			num--;
			if(num<0){
				clearInterval(timer);
				$('#hqyzm').css('color','#000');
				$('#hqyzm').text('获取验证码');
				$('#hqyzm').attr('disabled',false);
				num=60;

			}
		},1000)
	})	
	//错误提示框消失
	setTimeout(function(){
		$('#ts').hide();
	},1500);
})