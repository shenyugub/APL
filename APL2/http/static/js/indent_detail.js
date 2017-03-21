$(function(){
	var locat=location.href,
		s=locat.indexOf("?"); 
		t=locat.substring(s+1);
		arr=t.split("=");
		uid=arr[1];
	$.ajax({
		url:'https://apl.apluslabs.com/sudo/user_service_items/'+uid,
		type:'get',
		success:function(e){
			console.log(e);
			var data=e.item,
				str='';
			str+='<tr><td>订单号</td><td>'
					+data.id
					+'</td>'
					+'<td>订单状态</td><td>'
					+data.status
					+'</td></tr><tr><td>服务项</td><td>'
					+data.id
					+'</td>'
					+'<td>服务包类</td><td>'
					+data.id				
					+'</td></tr><tr><td>文件</td><td><a href="###" class="btn btn-default downL">下载</a></td><td>报价</td><td>'			
					+data.id
					+'</td></tr><tr><td>下单时间</td><td>'		
					+data.id				
					+'</td><td>报价说明</td><td>'		
					+data.id		
					+'</td></tr><tr><td>项目名称</td><td>'		
					+data.id				
					+'</td><td>备注</td><td>'
					+data.id
					+'</td></tr>';
			$('.tabs').find('tbody').html(str)

		}
	})

	$('#tj').on('click',function(){
		var txt=$('#text').val();
		alert(txt);
	})
})