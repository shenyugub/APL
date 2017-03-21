$(function(){
	/*$('.del').on('click',function(){
		$(this).parents('tr').remove();
	})*/
	//渲染表格
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/schedules',
			type:'get',
            dataType: 'json',
			success:function(e){
				console.log(e);
				/*var data=e.data,
					str='';
				for(var i in data){
					str+='<tr>'
						+'<td>'
							+data[i].stagenum		
						+'</td>'
						+'<td>'
							+data[i].stagename
						+'</td>'
						+'<td>'
							+data[i].stageser
						+'</td>'
						+'<td>'
							+data[i].times
						+'</td>'
						+'<td>'
							+data[i].founder
						+'</td>'
						+'<td>'
							+data[i].stagedes
						+'</td>'
						+'<td>'
							+data[i].statu
						+'</td>'
						+'<td>'
							+'<span class="del">删除</span>'	
						+'</td>'
						+'</tr>';
			}
			$('.mainTab').find('tbody').html(str);*/
		},
		error:function(){
			alert("请求数据失败");
		}
	})
})