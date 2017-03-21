$(function(){
	var obj={};
	$('#fbdp').on('click',function(){
		var na=$('#na').val(),
		    sj=$('#sj').val(),
		    textarea=$('#textarea').val();
		 obj.name=na;
		 obj.tel=sj;
		 obj.textarea=textarea;
		 console.log(obj);
		/*alert(na+"_"+sj+"_"+textarea);*/
	})
	$('#sj').on('blur',function(){
		var sjh=$('#sj').val(),
			reg=/^[1][358][0-9]{9}$/;
		if(reg.test(sjh)){
			$('#tssj').css('display','none');
		}else{
			$('#tssj').css('display','inline-block');
		}

	})
})