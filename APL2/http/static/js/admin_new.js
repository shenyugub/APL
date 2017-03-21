$(function(){
	$('#roles').on('change',function(){
		formK();
	})
	//切换角色,表单数据变为空
	function formK(){
		$('#firstName').val('');
		$('#email').val('');
		$('#perId').val('');
		$('#remarks').val('');
	}
	var obj={};
	$('#ktzh').on('click',function(){
		var type=$('#roles').val(),
			name=$('#firstName').val(),
			email=$('#email').val(),
			password=$('#pas').val();
		password=hex_md5(password);
		if(type=='项目方'){
			obj.type='Startup';
			obj.permissions=2;
		}else{
			obj.type='Investor';
			obj.permissions=4;
		}
		if(name!==''){
			obj.name=name;
		}else{
			if(obj.name){
				delete obj.name; 
			}
		}
		if(password!==''){
			obj.password=password;
		}else{
			if(obj.password){
				delete obj.password; 
			}
		}
		if(email!==''){
			obj.email=email;
		}else{
			if(obj.email){
				delete obj.email; 
			}
		}
		obj.confirmed=1;
		obj.initialized=0;
		obj.active=1;
		console.log(obj);
		//验证邮箱
		var reg=/^([0-9A-Za-z\-_\.]+)@([0-9a-z]+\.[a-z]{2,3}(\.[a-z]{2})?)$/g;		
		if(email==''){
			$('.emailTs').css('display','block');
			return false;
		}else{
			if(reg.test(email)==false){
				$('.emailTs').css('display','block');
				return false;
			}else{
				$('.emailTs').css('display','none');
				ajaxData(obj);
		}
		}
		
	})
	function ajaxData(obj){
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/users',
			data: JSON.stringify(obj),
			type:'post',
            dataType: 'json',
            contentType:'application/json',
			success:function(e){
				location.href='./admin_list.html';
			},
			error:function(){
				alert('获取数据失败');
			}
		})
	}
})