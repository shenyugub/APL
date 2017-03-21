$(function(){
	ajaxD();
	//渲染表格
	function ajaxD(){
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/phases',
			type:'get',
            dataType: 'json',
			success:function(e){
				var data=e.phases;
					str='';
				for(var i in data){
					str+='<tr>'
						+'<td style="width:12%">'
							+data[i].id		
						+'</td>'
						+'<td>'
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
				alert("请求数据失败");
			}
		})
	}
	//点击card遮罩层和弹出框出现
	$('.card').on('click',function(){
		var h=$('#tck').height(),
			w=$('#tck').width();
		$('#tck').css('marginLeft',-w/2+'px');
		$('#tck').css('marginTop',-h/2+'px');
		$('.mark').show();
		$('#tck').show();
		$('body').css('overflow','hidden');
		$.ajax({
				url:'https://apl.apluslabs.com/sudo/attachments',
				type:'get',
           		dataType: 'json',
            	success:function(e){
            		var data=e.attachments,
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
            	},
            	error:function(){
            		alert('失败');
            	}
			})	
			tabCon();	
	})
	//点击弹出框的确定
	function tabCon(){
		var obj={};
		$('.confirmBtn').unbind('click').click(function(){
			var stageName=$('#stageName').val(),
				stageDec=$('#stageDec').val(),
				sta=$('#sta option:selected').val(),
				text = $("input:checkbox[name='ck']:checked").map(function(index,elem) {
            		return $(elem).val();
       			 }).get().join(',');
			obj.name=stageName;
			obj.description=stageDec;
			obj.status=sta;
			obj.attachments=text;
			console.log(obj)
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/phases',
				data:JSON.stringify(obj),
				type:'post',
           		dataType:'json',
            	contentType:'application/json',
            	success:function(e){
            		console.log(e);
            		$('.mark').css('display','none');
            		$('#tck').css('display','none');
            		$('body').css('overflow','auto');
            		ajaxD();
            		zero();

            	},
            	error:function(){
            		alert('失败');
            	}
			})
		})	
	}
//弹出框数据清空
function zero(){
	$('#stageName').val('');
	$('#stageDec').val('');
}	
})