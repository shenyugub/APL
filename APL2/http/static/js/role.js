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
			url:'https://apl.apluslabs.com/sudo/roles',
			type:'get',
        	dataType: 'json',
			success:function(e){
				console.log(e)
				var data=e.roles,
					str='';
				for(var i in data){
					str+='<tr>'
						+'<td>'
							+data[i].name		
						+'</td>'
						+'<td>'
							+data[i].description
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
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/permissions',
			type:'get',
        	dataType: 'json',
        	success:function(e){
        		var data=e.permissions,
        			strs='';
        		for(var i in data){
        			strs+='<tr>'
						+'<td>'
							+data[i].id		
						+'</td>'
						+'<td>'
							+data[i].name
						+'</td>'				
						+'<td><input type="checkbox" name="ck" value="'+data[i].id+'"></td>'
						+'</tr>';
        		}
        		$('.tckTab').html(strs);
        		//阻止冒泡
					function stopBubble(e){
　　                    if(e&&e.stopPropagation){//非IE
　　                          e.stopPropagation();
　　                    }
　　                    else{//IE
　　                         window.event.cancelBubble=true;
　　                    }
　　                }
					$('input[type=checkbox]').on('click',function(e){
						stopBubble(e);
					})
        			$('.tckTab').find('tr').on('click',function(){
						if($(this).find('input').prop('checked')==true){
							$(this).find('input').prop('checked',false);
						}else{
							$(this).find('input').prop('checked',true);
						}
					})
				var h=$('#tck').height(),
				w=$('#tck').width();
				$('#tck').css('marginLeft',-w/2+'px');
				$('#tck').css('marginTop',-h/2+'px');		
        	}
		})
		getData();

	})
	//点击弹出框内的确认，获取数据
	function getData(){
		var obj={};
		$('.confirmBtn').unbind('click').click(function(){
			var names=$('#names').val(),
				jsms=$('#jsms').val(),
				status=$('#status option:selected').val(),
				text = $("input:checkbox[name='ck']:checked").map(function(index,elem) {
            		return $(elem).val();
       			 }).get().join(',');
			obj.name=names;
			obj.description=jsms;
			obj.status=status;
			obj.permissions=text;
			console.log(obj)
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/roles',
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