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
	$('#hy').on('blur',function(){
		var hy=$(this).val();
		if(hy=="请选择"){
			$(this).parent().next().css('display','inline-block');
		}else{
			$(this).parent().next().css('display','none');
		}
	})
	$('#confirm').on('click',function(){
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
		if($('#hy').val()=="请选择"){
			$('#hy').parent().next().css('display','inline-block');
		}else{
			$('#hy').parent().next().css('display','none');
		}
		var comname=$('#comname').val(),
		    comjs=$('#comjs').val(),
		    zcri=$('#zcri').val(),
		    zcdz=$('#zcdz').val();
		    hy=$('#hy').val();
		if(comname!="" && comjs!="" && zcri!="" && zcdz!="" && hy!="请选择"){
			obj.comname=comname;
			obj.comjs=comjs;
			obj.hy=hy;
			obj.zcri=zcri;
			obj.zcdz=zcdz;
			console.log(obj);
		}    
	})
})