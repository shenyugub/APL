$(function(){
	var obj={};
	$('.pd').on('blur',function(){
		var txt=$(this).val();
		if(txt==""){
			$(this).parent().next().css('display','inline-block');
		}else{
			$(this).parent().next().css('display','none');
		}
	});
	$('#qd2').on('click',function(){
		var arr=[];
		for(var i=0,len=$('.pd').length;i<len;i++){
			arr.push($('.pd').eq(i).val());
		}
		for(j=0;j<arr.length;j++){
			if(arr[j]==''){
				//console.log(j);
				$('.ts').eq(j).css('display','inline-block');
			}
		}
		var firstname=$('#firstname').val(),
		    email=$('#emails').val(),
		    tel=$('#tel').val(),
		    weixin=$('#weixin').val(),
		    zhiwei=$('#zhiwei').val(),
		    sex=$(':radio:checked').val();
		if(firstname!="" && email!="" && tel!="" && weixin!="" && zhiwei!=""){
			obj.firstname=firstname;
			obj.email=email;
			obj.tel=tel;
			obj.weixin=weixin;
			obj.zhiwei=zhiwei;
			obj.sex=sex;
			console.log(obj);
		}    
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