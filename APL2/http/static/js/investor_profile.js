$(function(){
	var obj={};
	$('#qd').on('click',function(){
		var firstname=$('#firstname').val(),
		    email=$('#email').text(),
		    tel=$('#tel').val(),
		    wxh=$('#wxh').val(),
		    zhiwei=$('#zhiwei').val(),
		    sex=$(':radio:checked').val();
		obj.firstname=firstname;
		obj.email=email;
		obj.tel=tel;
		obj.wxh=wxh;
		obj.zhiwei=zhiwei;
		obj.sex=sex;
		console.log(obj);
	})
	$('#tel').on('blur',function(){
		var con=$(this).val(),
			reg=/^[1][358][0-9]{9}$/;
			if(reg.test(con)){
				$(this).parent().next().css('display','none');
			}else{
				$(this).parent().next().css('display','inline-block');
			}
	})
})