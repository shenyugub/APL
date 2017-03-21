$(function(){
	//页面渲染的表单
	function drawTab(){
		var box='';
				box+='<form class="form-horizontal" role="form">'
		            		+'<div class="form-group">'
		                 			+'<label class="col-sm-3 control-label">身份名称：</label>'
		                  			+'<div class="col-sm-6">'
		                      			+'<input type="text" class="form-control" id="identityName">'
		                  			+'</div>'
		            		+'</div>'
		            		+'<div class="form-group">'
		                  			+'<label class="col-sm-3 control-label">身份描述：</label>'
		                  				+'<div class="col-sm-6">'
		                      				+'<input type="text" class="form-control" id="roles">'
		                  				+'</div>'
		            		+'</div>'
		            		+'<div class="form-group">'
		             	 			+'<label class="col-sm-3 control-label">状态：</label>'
		              	 					+'<div class="col-sm-6">'
		                  						+'<select class="form-control" id="statu">'
		                    							+'<option>启用</option>'
		                    							+'<option>禁用</option>'
		                						+'</select>'
		              						+'</div>'
		          			+'</div>'
					+'</form>';
				$('#tck_box').html(box);
	}
	//点击创建身份渲染的表单
	$('.card').on('click',function(){
		drawTab();
		$('#tck').find('h5').text("创建身份");
		$('.mark').show();
		$('#tck').show();
		getData();
	})
	//请求数据
	$.ajax({
		url:window.location.protocol + '//'+ window.location.host + "/sudo/",
		data:'',
		type:'post',
        dataType: 'json',
        contentType:'application/json',
		success:function(e){
			console.log(e);
			/*var data=e.data,
				str='';
			for(var i in data){
				str+='<tr>'
						+'<td>'
							+data[i].identityName		
						+'</td>'
						+'<td>'
							+data[i].roles
						+'</td>'
						+'<td>'
							+data[i].times
						+'</td>'
						+'<td>'
							+data[i].statu
						+'</td>'
						+'<td>'
							+'<span class="amend">修改</span> <span class="allocation">权限配置</span>'	
						+'</td>'
						+'</tr>'
			}
			$('.mainTab').find('tbody').html(str);*/
			//点击修改时渲染的表单
			$('.amend').on('click',function(){
				//获取这一行的数据????????????????????????????????????????????????
				var identityName=$(this).parents('tr').children('td').get(0).innerHTML;
				var roles=$(this).parents('tr').children('td').get(1).innerHTML;
				var statu=$(this).parents('tr').children('td').get(3).innerHTML;
				//表单的渲染
				drawTab();
				$('#identityName').val(identityName);
				$('#roles').val(roles);
				$('#statu').val(statu);
				$('#tck').find('h5').text("修改角色");
				$('.mark').show();
				$('#tck').show();
				getData();
			})
			//点击权限配置渲染表格
			$('.allocation').on('click',function(){
				$('#tck').find('h5').text("权限配置");
				var box='';
				box+='<table class="table table-hover table-bordered table-striped tab">'
						+'<thead>'
							+'<tr>'
								+'<td>'
									+'模块名称'
								+'</td>'
								+'<td>'
									+'<input type="checkbox" id="ck1"><label for="ck1">&nbsp;分配权限</label>'
								+'</td>'
							+'</tr>'
						+'</thead>'
						+'<tbody>'
							+'<tr>'
								+'<td>'
									+'个人中心'
								+'</td>'
								+'<td>'
									+'<input type="checkbox" id="ck2"><label for="ck2">&nbsp;分配权限</label>'
								+'</td>'
							+'</tr>'
							+'<tr>'
								+'<td>'
									+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;项目管理'
								+'</td>'
								+'<td>'
									+'<input type="checkbox" id="ck3"><label for="ck3">&nbsp;分配权限</label>'
								+'</td>'
							+'</tr>'
							+'<tr>'
								+'<td>'
									+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发布项目'
								+'</td>'
								+'<td>'
									+'<input type="checkbox" id="ck4"><label for="ck4">&nbsp;分配权限</label>'
								+'</td>'
							+'</tr>'
							+'<tr>'
								+'<td>'
									+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;约谈记录'
								+'</td>'
								+'<td>'
									+'<input type="checkbox" id="ck5"><label for="ck5">&nbsp;分配权限</label>'
								+'</td>'
							+'</tr>'
							+'<tr>'
								+'<td>'
									+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;安全设置'
								+'</td>'
								+'<td>'
									+'<input type="checkbox" id="ck6"><label for="ck6">&nbsp;分配权限</label>'
								+'</td>'
							+'</tr>'
							+'<tr>'
								+'<td>'
									+'全部项目'
								+'</td>'
								+'<td>'
									+'<input type="checkbox" id="ck7"><label for="ck7">&nbsp;分配权限</label>'
								+'</td>'
							+'</tr>'
							+'<tr>'
								+'<td>'
									+'投资人&nbsp;&nbsp;&nbsp;'
								+'</td>'
								+'<td>'
									+'<input type="checkbox" id="ck8"><label for="ck8">&nbsp;分配权限</label>'
								+'</td>'
							+'</tr>'
						+'</tbody>'
					+'</table>'
				$('#tck_box').html(box);	
				$('.mark').show();
				$('#tck').show();
			})
		},
		error:function(){
			alert("请求数据失败");
		}
	})
//点击弹出框内的确认，获取弹出框内信息
function getData(){
	var obj={};
	$('.confirmBtn').on('click',function(){
		var identityName=$('#identityName').val(),
			roles=$('#roles').val(),
			statu=$('#statu').val();
		obj.identityName=identityName;
		obj.roles=roles;
		obj.statu=statu;
		console.log(obj);
	/*alert(identityName+'_'+roles+'_'+statu);*/
	})
}


	
	
})