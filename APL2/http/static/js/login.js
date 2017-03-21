$(function(){
	var obj={};
	$('#dl').on('click',function(){
		var email=$('#email').val(),
			password=$('#password').val(),
			yanzhengma=$('#yanzhengma').val();
		if(email!="" && password!="" && yanzhengma!=""){
			obj.email=email;
			obj.password=password;
			obj.yanzhengma=yanzhengma;
			console.log(obj);
			location.href="./startup/profile.html";
		}
	})	
})