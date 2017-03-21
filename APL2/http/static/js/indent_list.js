$(function(){
	tabData();
	//点击查询获取数据
	$('#search').on('click',function(){
		tabData();
	})
	//渲染表格数据
	function tabData(){
		$('#tt').datagrid({
				loader:fn,
				singleSelect: true,
				nowrap:false,
				loadMsg: '数据加载中.....',
				frozenColumns:[[
					{field:'id',title:'订单号',align:'center',width:'8%'},
					{field:'service_name',title:'服务项',align:'center',width:'16%'},
				]],
				columns:[[
					{field:'gmt_create',title:'下单时间',align:'center',width:'30%'},
					{field:'status',title:'订单状态',align:'center',width:'16%'},
					{field:'price',title:'订单金额',align:'center',width:'16%'},
					{field:'cz',align:'center',title:'操作',width:'16%',
						formatter: function (vales ,row, index ) {
							var a = '<a href="./indent_detail.html?uid='+row.id+'">反馈详情</a>';
							return a;
						}
					}
				]],
				onLoadSuccess:function(){
					var script=document.createElement('script');
					script.src='../../static/js/structure.js';
					document.body.appendChild(script);						
				}
		})
	}
	function fn(param,success,error){
		var transaction=$('#transaction').val(),
			condition=$('#condition option:selected').val(),
			proName=$('#proName').val(),
			sersort=$('#sersort option:selected').val(),
			services=$('#services').val(),
			serName=$('#serName').val(),
			startT=$('#startT').val(),
			endT=$('#endT').val();
		var obj={};
		if(transaction!==''){
			obj.id=transaction;
		}
		if(condition!=='请选择'){
			obj.status=condition;
		}
		if(proName!==''){
			obj.project_name=proName;
		}
		if(services!==''){
			obj.service_item=services;
		}
		if(sersort!=='请选择'){
			obj.service_category=sersort;
		}
		if(serName!==''){
			obj.service_name=serName;
		}
		if(startT!==''){
			obj.starttime=startT;
		}
		if(endT!==''){
			obj.endtime=endT;
		}
		/*console.log(obj);*/
		var url1 = 'https://apl.apluslabs.com/sudo/user_service_items',
    　　　　ajax1 = $.ajax(
      　　 　　 {
         　　　　  url:url1,
				   data:obj,
			       type:'get'
        　　　　}
 　　  　　 );

　　　　$.when(ajax1).done(function(e){
			var data=e.items;
			console.log(data);
			for(var i in data){
				if(data[i].status=='ServiceStatus.Submitting'){
					data[i].status='待提交'
				}
				if(data[i].status=='ServiceStatus.Ignoring'){
					data[i].status='请求忽略'
				}
				if(data[i].status=='ServiceStatus.Ignored'){
					data[i].status='已忽略'
				}
				if(data[i].status=='ServiceStatus.Rejected'){
					data[i].status='已驳回'
				}
				if(data[i].status=='ServiceStatus.Submitted'){
					data[i].status='已提交'
				}
				if(data[i].status=='ServiceStatus.Confirmed'){
					data[i].status='已确认'
				}
				if(data[i].status=='ServiceStatus.Finished'){
					data[i].status='已完成'
				}
			}
   　　　　 success(data);
   			qk();

　　　　}).fail(function(){
　　
   　　　　 alert("fail");
    
　　　　});
	}
function qk(){
	$('#transaction').val(''),
	$('#proName').val('');
	$('#services').val('');
	$('#serName').val('');
	$('#startT').val('');
	$('#endT').val('');
}
	
})
