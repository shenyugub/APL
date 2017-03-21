$(function(){
	tabData();
	//点击查询获取表单数据
	$('#search').on('click',function(){
		tabData();
	})
	//渲染表格数据
	function tabData(){
		$('#projectTab').datagrid({
				loader:fn,
				url:'https://apl.apluslabs.com/sudo/projects',
				singleSelect: true,
				loadMsg: '数据加载中.....',
				frozenColumns:[[
					{field:'id',title:'项目编号',align:'center'},
					{field:'name',title:'项目名称',align:'center'},
				]],
				columns:[[
					{field:'contact_name',title:'负责人',align:'center'},
					{field:'contact_phone',title:'手机号',align:'center'},
					{field:'gmt_create',title:'创建时间',align:'center'},
					{field:'industry',title:'所在行业',align:'center'},
					{field:'phase',title:'所在阶段',align:'center'},
					{field:'duration',title:'本阶段预计开发时间',align:'center'},				
					{field:'audit',align:'center',title:'审核',width:'100px',
						formatter: function (vales ,row, index ) {
							var bh=row.id;
							var a = '<a class="pass" data_id="'+bh+'"> </a><a class="reject" data_id="'+bh+'"></a>';
							return a;
						}
					}
				]],
				onLoadSuccess:function(data){
					var script=document.createElement('script');
					script.src='../../static/js/structure.js';
					document.body.appendChild(script);
					console.log(data.rows);
					for(var i in data.rows){
						if(data.rows[i].status=='ProjectStatus.Verifying'){
							$($('.pass')[i]).text('通过');	
							$($('.reject')[i]).text('驳回');	
						}else if(data.rows[i].status=='ProjectStatus.Editing'){
							$($('.pass')[i]).text('编辑中');	
						}else if(data.rows[i].status=='ProjectStatus.Rejected'){
							$($('.pass')[i]).text('已驳回');	
						}else if(data.rows[i].status=='ProjectStatus.Accepted'){
							$($('.pass')[i]).text('已通过');
						}
					}
					//阻止冒泡
					function stopBubble(e){
　　                    if(e&&e.stopPropagation){//非IE
　　                          e.stopPropagation();
　　                    }
　　                    else{//IE
　　                         window.event.cancelBubble=true;
　　                    }
　　                }
					var aObj={};
					//点击通过
					$('.pass').on('click',function(e){
						stopBubble(e);
						if($(this).text()=='通过'){
							aObj.status='Accepted';
						}else if($(this).text()=='已通过'){
							$(this).siblings().remove();
							return false;
						}else if($(this).text()=='已驳回'){
							return false;
						}
						var uid=$(this).attr('data_id');
						ajaxD(uid,aObj);
						$(this).text("已通过");
					})
					//点击驳回
					$('.reject').on('click',function(e){
						stopBubble(e);
						if($(this).text()=='驳回'){
							aObj.status='Rejected';
						}else if($(this).text()=='已通过'){
							return false;
						}else if($(this).text()=='已驳回'){
							$(this).siblings().remove();
							return false;
						}
						var uid=$(this).attr('data_id');
						ajaxD(uid,aObj);
						$(this).text("已驳回");
					})
					function ajaxD(uid,aObj){
						$.ajax({
							url:'https://apl.apluslabs.com/sudo/projects/'+uid,
							data: JSON.stringify(aObj),
							type:'post',
                            dataType: 'json',
            			 	contentType:'application/json',
            			 	success:function(e){
            			 		console.log(e)
            			 	},
            			 	error:function(){
            			 		alert("失败");
            			 	}
						})
					}
				},
				onClickRow: function (rowIndex, rowData) {
					/*console.log(rowData.id)*/
					location.href='./project_detail.html?uid='+rowData.id;
				}
		})	
	}
	function fn(param,success,error){
		var itemlNum=$('#itemlNum').val(),
			itemName=$('#itemName').val(),
			principal=$('#principal').val(),
			industry=$('#industry option:selected').text(),
			stage=$('#stage option:selected').text(),
			tele=$('#tele').val(),
			startT=$('#startT').val(),
			endT=$('#endT').val();
		var obj={};
		if(itemlNum!==''){
			obj.id=itemlNum;
		}
		if(itemName!==''){
			obj.name=itemName;
		}
		if(principal!==''){
			obj.contact_name=principal;
		}
		if(tele!==''){
			obj.contact_phone=tele;
		}
		if(startT!==''){
			obj.starttime=startT;
		}
		if(endT!==''){
			obj.endtime=endT;
		}		
		if(industry!=='请选择'){
			obj.industry=industry;
		}
		if(stage!=='请选择'){
			obj.phase=stage;
		}	
		var url1 = 'https://apl.apluslabs.com/sudo/projects',
    　　　　ajax1 = $.ajax(
      　　 　　 {
         　　　　   url : url1,
         			type:'get',
         			data: obj
        　　　　}
 　　  　　 );

　　　　$.when(ajax1).done(function(e){
			var data=e.projects;
			console.log(e);
			for(var i in data){
				if(data[i].industry=='Industry.IntelligentMake'){
					data[i].industry='智能制造';
				}else if(data[i].industry=='Industry.IntelligentHardware'){
					data[i].industry='智能硬件';
				}else if(data[i].industry=='Industry.AI'){
					data[i].industry='人工智能';
				}else if(data[i].industry=='Industry.IoT'){
					data[i].industry='物联网';
				}else if(data[i].industry=='Industry.Sensor'){
					data[i].industry='传感器技术';
				}else if(data[i].industry=='Industry.NewMaterial'){
					data[i].industry='新材料新能源';
				}else if(data[i].industry=='Industry.ArVr'){
					data[i].industry='AR/VR';
				}else if(data[i].industry=='Industry.Drone'){
					data[i].industry='无人机';
				}else if(data[i].industry=='Industry.BigData'){
					data[i].industry='大数据';
				}else if(data[i].industry=='Industry.Medicine'){
					data[i].industry='医疗';
				}else if(data[i].industry=='Industry.Education'){
					data[i].industry='教育';
				}else if(data[i].industry=='Industry.Finance'){
					data[i].industry='金融';
				}else if(data[i].industry=='Industry.ConsumptionUpgrading'){
					data[i].industry='消费升级';
				}else if(data[i].industry=='Industry.O2O'){
					data[i].industry='O2O';
				}else if(data[i].industry=='Industry.BlackTechnology'){
					data[i].industry='黑科技';
				}else{
					data[i].industry='其他行业';
				}
			}
   　　　　 success(data);
   			qk();

　　　　}).fail(function(){
　　
   　　　　 alert("fail");
    
　　　　});
	}
function qk(){
	$('#itemlNum').val(''),
	$('#itemName').val('');
	$('#principal').val('');
	$('#tele').val('');
	$('#startT').val('');
	$('#endT').val('');
}
})
	
	
