$(function(){
	/*$('.del').on('click',function(){
		$(this).parents('tr').remove();
	})*/
	//渲染表格
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/comments',
			type:'get',
            dataType: 'json',
			success:function(e){
				var data=e.comments,
					str='';
				console.log(data)
				for(var i in data){
					str+='<tr>'
						+'<td>'
							+data[i].id
						+'</td>'
						+'<td>'
							+data[i].project_name
						+'</td>'
						+'<td>'
							+data[i].author_name
						+'</td>'
						+'<td>'
							+data[i].content
						+'</td>'
						+'<td>'
							+data[i].gmt_create
						+'</td>'
						+'</tr>';
			}
			$('.mainTab').find('tbody').html(str);
			var script=document.createElement('script');
				script.src='../../static/js/structure.js';
				document.body.appendChild(script);
		},
		error:function(){
			alert("请求数据失败");
		}
	})
})