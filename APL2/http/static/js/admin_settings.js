$(function(){
	var obj={};
	$('#confirm').on('click',function(){
		var oldPsw=$('#oldPsw').val(),
		    newPsw=$('#newPsw').val(),
		    repePsw=$('#repePsw').val();
		if(newPsw!=repePsw){
			$('.tsBox').css('display','block');
		}else{
			$('.tsBox').css('display','none');
			old_pwd=hex_md5(oldPsw);
			new_pwd=hex_md5(newPsw);
			obj.old_pwd=old_pwd;
			obj.new_pwd=new_pwd;
			//console.log(obj);
			$.ajax({
				url:window.location.protocol + '//'+ window.location.host + "/sudo/reset_password",
				data: JSON.stringify(obj),
				type:'post',
                dataType: 'json',
                contentType:'application/json',
				success:function(e){
					$('.tooltips').css('display','block');
					if(e.message){//修改密码的提示  修改成功 失败  you are not admin
						$('.tooltips').text(e.message);
					}else{
						$('.tooltips').text(e);
					}
					setTimeout(function(){
						$('.tooltips').css('display','none');
					},1000)
				},
				error:function(jqXHR,textStatus,errorThrown){
					alert(errorThrown);
				}
			})
		}
	})

})