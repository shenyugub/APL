$(function(){
	ajaxs();
	//弹出框数据清空
	function zero(){
		$('#names').val('');
		$('#jsms').val('');
	}
	//获取数据
	function ajaxs(){
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/permissions',
			type:'get',
        	dataType: 'json',
			success:function(e){
				console.log(e)
				var data=e.permissions,
					str='';
				for(var i in data){
					if(data[i].status==true){
						data[i].status='启用';
					}else{
						data[i].status='禁用';
					}
					str+='<tr>'
						+'<td>'
							+data[i].id		
						+'</td>'
						+'<td>'
							+data[i].name
						+'</td>'
						+'<td>'
							+data[i].description
						+'</td>'
						+'<td style="color:#2aabd2">'
							+data[i].status
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
		$('.confirmBtn').unbind('click').click(function(){
			var names=$('#names').val(),
				jsms=$('#jsms').val(),
				status=parseInt($('#status option:selected').val());
			obj.name=names;
			obj.description=jsms;
			obj.status=status;
			console.log(obj)
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/permissions',
				data:JSON.stringify(obj),
				type:'post',
           		dataType:'json',
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