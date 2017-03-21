$(function(){
	tabData();
	//点击查询获取表单数据
	$('#search').on('click',function(){
		tabData();
	})
	//渲染表格数据
	function tabData(){
		var obj={};
		var condition=$('#condition option:selected').val(),
			names=$('#names').val(),
			sTime=$('#sTime').val(),
			eTime=$('#eTime').val();
			if(condition!=='请选择'){
				obj.status=condition;
			}
			if(names!==''){
				obj.project_name=names;
			}
			if(sTime!==''){
				obj.starttime=sTime;
			}
			if(eTime!==''){
				obj.endtime=eTime;
			}
			console.log(obj);	
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/user_attachments',
			data:obj,
			type:'get',
            dataType: 'json',
			success:function(e){
				qk();
				console.log(e);
				var data=e.attachments,
					str='';
				for(var i in data){
					if(data[i].status=='AttachmentStatus.Submitting'){
						data[i].status='待提交';
					}else if(data[i].status=='AttachmentStatus.Submitted'){
						data[i].status='已提交';
					}else if(data[i].status=='AttachmentStatus.Rejected'){
						data[i].status='已驳回';
					}else if(data[i].status=='AttachmentStatus.Confirmed'){
						data[i].status='已确认';
					}
					str+='<tr class="'+data[i].ppid+'" data_id="'+data[i].attachment_id+'">'
						+'<td>'
							+data[i].id		
						+'</td>'
						+'<td>'
							+data[i].project_name		
						+'</td>'
						+'<td>'
							+data[i].ppid
						+'</td>'
						+'<td>'
							+data[i].attachment_name
						+'</td>'
						+'<td>'
							+data[i].gmt_create
						+'</td>'
						+'<td>'
							+data[i].status
						+'</td>'
						+'<td>'
							+'<span class="pass" data_id="'+data[i].id+'" data_ppid="'+data[i].ppid+'" data_attachment_id="'+data[i].attachment_id+'">通过</span>'	
						+'</td>'
						+'</tr>';
			}
			$('.mainTab').find('tbody').html(str);
			var script=document.createElement('script');
				script.src='../../static/js/structure.js';
				document.body.appendChild(script);
				var w=$('.container-fluid').width();
				var h=$('.container-fluid').height()+$('.head').height();
				$('.mark').width(w);
				$('.mark').height(h);
				//阻止冒泡
				function stopBubble(e){
　　                if(e&&e.stopPropagation){//非IE
　　                   e.stopPropagation();
　　                }
　　                else{//IE
　　                   window.event.cancelBubble=true;
　　                }
　　               }
			var obje={};
			$('.pass').on('click',function(e){
				stopBubble(e);
				var uid=$(this).attr('data_id');
				var ppid=$(this).attr('data_ppid');
				var attachment_id=$(this).attr('data_attachment_id');
				$(this).text()=='通过';
				obje.status='Confirmed';
				obje.ppid=ppid;
				obje.attachment_id=attachment_id;
				console.log(obje);
				ajaxs(uid,obje,$(this));
			})
			function ajaxs(uid,obje,s){
				$.ajax({
					url:'https://apl.apluslabs.com/sudo/user_attachments/'+uid,
					data: JSON.stringify(obje),
					type:'post',
           			dataType: 'json',
            		contentType:'application/json',
            		success:function(e){
            			$(s).text("已通过");
            		},
            		error:function(){
            			alert("失败");
            		}
				})
			}
			//点击表格行出现弹出框
			$('.mainTab').find('tr:not(:first)').on('click',function(){
				var h=$('#tck').height(),
					w=$('#tck').width();
				$('#tck').css('marginLeft',-w/2+'px');
				$('#tck').css('marginTop',-h/2+'px');
				$('.mark').show();
				$('#tck').show();
				$('body').css('overflow','hidden');
				var ppid=$(this).attr('class');
				var attachment_id=$(this).attr('data_attachment_id');
				tc(ppid,attachment_id);
				//alert(ppid)
			})	
			//点击弹出框发送按钮
			function tc(ppid,attachment_id){
				var aObj={};
				$('#upl').on('click',function(){
					var txt=$('#txt').val();
					aObj.ppid=ppid;
					aObj.attachment_id=attachment_id;
					if(txt!==''){
						aObj.comment=txt;
					}
					$.ajax({
						url:'https://apl.apluslabs.com/sudo/user_attachments',
						data: JSON.stringify(aObj),
						type:'post',
           				dataType: 'json',
            			contentType:'application/json',
            			success:function(e){
            				console.log(e);
            				$('.mark').hide();
            				$('#tck').hide();
            				$('#txt').val('');
            			},
            			error:function(){
            				alert("失败");
            			}
					})
				})
			}
				
		},
		error:function(){
			alert("请求数据失败");
		}
	})
	}
	$('.cancel').on('click',function(){
		$('.mark').hide();
        $('#tck').hide();
		$('body').css('overflow','auto');
		$('#tx').val('');
	})
function qk(){
	$('#names').val(''),
	$('#sTime').val('');
	$('#eTime').val('');
}
	
})