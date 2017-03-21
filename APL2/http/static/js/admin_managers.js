$(function(){
	ajaxs();
	//弹出框数据清空
	function zero(){
		$('#names').val('');
		$('#email').val('');
		$('#pas').val('');
	}
	//获取数据
	function ajaxs(){
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/admins',
			type:'get',
        	dataType: 'json',
			success:function(e){
				var data=e.admins,
					str='';
				for(var i in data){
					str+='<tr>'
						+'<td>'
							+data[i].name		
						+'</td>'
						+'<td>'
							+data[i].dept_name
						+'</td>'
						+'<td>'
							+data[i].role_name
						+'</td>'
						+'<td>'
							+data[i].latest
						+'</td>'
						+'<td>'
							+'<span class="an"></span>'
						+'</td>'
						+'</tr>';
				}
				$('.mainTab').find('tbody').html(str);
				var script=document.createElement('script');
				script.src='../../static/js/structure.js';
				document.body.appendChild(script);
				for(var i in data){
					if(data[i].status==true){
						$($('.an')[i]).text("禁用");
					}else{
						$($('.an')[i]).text("启用");
					}
				}
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
		ajax('departments','bm');
		ajax('roles','js');
		function ajax(uid,con){
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/'+uid,
				type:'get',
           		dataType: 'json',
           		success:function(e){
           			var d=e[uid],
            			s='';
            		for(var i in d){
            			s+='<option value="'+d[i].id+'">'+d[i].name+'</option>';
            		}
            		$('#'+con).html(s);
           		},
           		error:function(){
           			alert("失败");
           		}
       		})
		}
		getData();
	})
	//点击弹出框内的确认，获取数据
	function getData(){
		var obj={};
		$('.confirmBtn').unbind('click').click(function(){
			var names=$('#names').val(),
				email=$('#email').val(),
				pas=$('#pas').val(),
				bm=$('#bm option:selected').val(),
				js=$('#js option:selected').val(),
				status=parseInt($('#status option:selected').val());
			pas=hex_md5(pas);
			obj.name=names;
			obj.email=email;
			obj.password=pas;
			obj.dept_id=bm;
			obj.role_id=js;
			obj.status=status;
			console.log(obj)
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/admins',
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