$(function(){
	//ajax请求验证码图片
	$(window).on('load',function(){
		ajaxImg();
	})
	$('#getImg').on('click',function(){
		ajaxImg();
	})
	function ajaxImg(){

	    u = window.location.protocol + '//'+ window.location.host + "/v_code";
		$.ajax({
			url: u,
			success:function(e){
				var src=e;
				$('#getImg').find('img').attr('src',src);
			},
			error:function(){


				alert("获取验证码失败22ddd2");
			}
		})
	}
	//后台点击登录把密码加密
	var obj={};
	$('#dls').on('click',function(){
		//获取form值 并把密码加密
		var userName=$('#userName').val(),
	    	password=$('#psw').val(),
	    	vcode=$('#vcode').val(),
       		password=hex_md5(password);
			// $('#psw').val(password);
			obj.username=userName;
			obj.password=password;
			obj.vcode=vcode;

			//传送数据
			$.ajax({
				url: window.location.protocol + '//'+ window.location.host + "/sudo/",
				data: JSON.stringify(obj),
				type:"post",
                dataType: 'json',
                contentType:'application/json',
				success:function(e){
					if(e.message=='登陆成功'){
						location.href='./project_list.html';
					}
				},
				error:function(jqXHR,textStatus,errorThrown){
					alert(errorThrown);
				}
			})
	})
	//前台点击登录把密码加密
	$('#dl').on('click',function(){
		var password=$('#psw').val();
        password=hex_md5(password);
		$('#psw').val(password);

	})	
	//错误提示框消失
	setTimeout(function(){
		$('#ts').hide();
	},1500);


})