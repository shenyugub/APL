$(function(){
	var ppid=$('.ppid').attr('id');
	//弹出框居中
	function tcks(){
		var h=$('#tck').height(),
			w=$('#tck').width();
		$('#tck').css('marginLeft',-w/2+'px');
		$('#tck').css('marginTop',-h/2+'px');
		$('.mark').show();
		$('#tck').show();
		$('body').css('overflow','hidden');

	}
	//点击定制服务跳转页面
	$('.card').eq(1).on('click',function(){
		$('#tck').find('h5').text('定制服务');
		$('#tck').find('.div').eq(1).css('display','block').siblings('.div').css('display','none');
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/service_categories',
			type:'get',
			success:function(e){
				console.log(e);
				var d=e.service_category_list,
					sel='';
				for(var i in d){
					sel+='<option value="'+d[i].id+'">'+d[i].name+'</option>'
				}
				$('#xqfl').html(sel);
				$('.confirmBtn').css({'position':'static'});
				$('.cancel').css({'position':'static'});
			},
			error:function(){
				alert("定制服务失败");
			}
		})
		tcks();
		dz();
	})
	//点击系统服务渲染弹出框
	$('.card').eq(0).on('click',function(){
		$('#tck').find('h5').text('系统服务');
		$('#tck').find('.div').eq(0).css('display','block').siblings('.div').css('display','none');
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/service_items',
			type:'get',
			success:function(e){
				console.log(e);
				var data=e.service_item_list,
					str='';
				for(var i in data){
					str+='<tr>'
						+'<td>'
							+data[i].id		
						+'</td>'
						+'<td>'
							+data[i].name
						+'</td>'
						+'<td>'
							+data[i].desc
						+'</td>'
						+'<td>'
							+data[i].category_name
						+'<td>'
							+data[i].price
						+'</td>'
						+'<td>'
							+'<input type="checkbox" name="tk" value="'+data[i].id+'">'
						+'</td>'
						+'</tr>';
				}
				$('.tckTab').find('tbody').html(str);
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
				tcks();
				$('.confirmBtn').css({'position':'fixed','bottom':'20px','left':'40%'});
				$('.cancel').css({'position':'fixed','bottom':'20px','left':'50%'});
			},
			error:function(){
				alert("tab失败");
			}
		})
		tcks();
		tabCon();
	})
	//点击取消
	$('.cancel').on('click',function(){
		$('.mark').hide();
		$('#tck').hide();
		$('body').css('overflow','auto');
		qk();
	})
	//点击取消
	$('.cancels').on('click',function(){
		$('.mark').hide();
		$('#tck').hide();
		$('body').css('overflow','auto');
		qk();
	})
	//点击弹出框的确定
	function tabCon(){
		var obj={};
		$('.confirmBtn').unbind('click').click(function(){
			var text = $("input:checkbox[name='tk']:checked").map(function(index,elem) {
            		return $(elem).val();
       			 }).get().join(',');
			obj.service_id=text;
			obj.ppid=ppid;
			console.log(obj)
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/user_service_items',
				data:JSON.stringify(obj),
				type:'post',
           		dataType:'json',
            	contentType:'application/json',
            	success:function(e){
            		console.log(e);
            		$('.mark').css('display','none');
            		$('#tck').css('display','none');
            		$('body').css('overflow','auto');
            		qk();
              	},
            	error:function(){
            		alert('yi失败');
            	}
			})
		})	
	}
	//点定制服务弹出框的确定
	function dz(){
		var nObj={};
		$('.confirmBtn').unbind('click').click(function(){
			var title=$('#titles').val(),
				xqfl=parseInt($('#xqfl option:selected').val()),
				xqnr=$('#xqnr').val();
			if(title!==''){
				nObj.title=title;
			}
			if(xqfl!=='请选择'){
				nObj.category_id=xqfl;
			}
			if(xqnr!==''){
				nObj.description=xqnr;
			}
			nObj.ppid=ppid;
			console.log(nObj)
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/custom_service_items',
				data:JSON.stringify(nObj),
				type:'post',
           		dataType:'json',
            	contentType:'application/json',
            	success:function(e){
            		console.log(e);
            		$('.mark').css('display','none');
            		$('#tck').css('display','none');
            		$('body').css('overflow','auto');
            		qk();
              	},
            	error:function(){
            		alert('er失败');
            	}
			})
		})
	}
	//点击提交确认
	function qr(s){
		var aObj={};
		$('.confirmBtn').unbind('click').click(function(){
			var text=$('#textareaTex').val();
			if(text!==''){
				aObj.comment=text;
			}
			aObj.ppid=ppid;
            aObj.attachment_id = s;
			console.log(aObj)
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/user_attachments',
				data:JSON.stringify(aObj),
				type:'post',
           		dataType:'json',
            	contentType:'application/json',
            	success:function(e){
            		console.log(e);
            		$('.mark').css('display','none');
            		$('#tck').css('display','none');
            		$('body').css('overflow','auto');
            		qk();
              	},
            	error:function(){
            		alert('提交失败');
            	}
			})
		})
	}
	
function qk(){
	$('.tckTab').find('input').prop('checked',false);
	$('#titles').val('');
	$('#xqnr').val('');
	$('#textareaTex').val('');
	/*var file = $("#files") 
	file.after(file.clone().val("")); 
	file.remove(); */
}
//点击提交
$('.jl').on('click',function(){
	$('#tck').find('h5').text('提交');
	$('#tck').find('.div').eq(2).css('display','block').siblings('.div').css('display','none');
	$('.confirmBtn').css({'position':'static'});
	$('.cancel').css({'position':'static'});
	var s=$(this).attr('id');
	tcks();
	qr(s);
})
})