$(function(){
	ajaxs();
	//获取数据
	function ajaxs(){
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/attachments',
			type:'get',
        	dataType: 'json',
			success:function(e){
				var data=e.attachments,
					str='';
				for(var i in data){
					str+='<tr>'
						+'<td>'
							+data[i].id		
						+'</td>'
						+'<td style="text-align:left;padding-left:3%">'
							+data[i].name
						+'</td>'
						+'<td>'
							+data[i].description
						+'</td>'
						+'</tr>';
				}
				$('.mainTab').find('tbody').html(str);
				var script=document.createElement('script');
				script.src='../../static/js/structure.js';
				document.body.appendChild(script);
			},
			error:function(){
				alert('获取数据有误');
			}
		})
	}
	//弹出框数据清空
	function zero(){
		$('#sort').val('');
		$('#describe').val('');
	}	

	$('.card').on('click',function(){
		var h=$('#tck').height(),
			w=$('#tck').width();
		$('#tck').css('marginLeft',-w/2+'px');
		$('#tck').css('marginTop',-h/2+'px');
		$('.mark').show();
		$('#tck').show();
		$('body').css('overflow','hidden');
		getData();
	})
	//点击弹出框内的确认，获取数据
	function getData(){
		var obj={};
		$('#abc').unbind('click').click(function(){
			var sort=$('#sort').val(),
				describe=$('#describe').val();
			obj.name=sort;
			obj.description=describe;
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/attachments',
				data: JSON.stringify(obj),
				type:'post',
           		dataType: 'json',
            	contentType:'application/json',
            	success:function(e){
            		console.log(e);
            		$('.mark').css('display','none');
            		$('#tck').css('display','none');
            		$('body').css('overflow','auto');
            		ajaxs();
            		zero();
            	},
            	error:function(){
            		alert('失败');
            	}
			})
		})		
	}	
})