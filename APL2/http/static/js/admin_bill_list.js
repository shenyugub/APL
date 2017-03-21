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
					{field:'id',title:'订单号',align:'center',width:'10%'},
				]],
				columns:[[
					{field:'project_name',title:'项目名称',align:'center',width:'26%'},
					{field:'service_name',title:'服务名称',align:'center',width:'26%'},					
					{field:'price',title:'金额',align:'center',width:'10%'},
					{field:'gmt_create',title:'下单时间',align:'center',width:'30%'},
				]],
				onLoadSuccess:function(){
					var script=document.createElement('script');
					script.src='../../static/js/structure.js';
					document.body.appendChild(script);
					$('.dis').on('click',function(){
						if($(this).text()=="禁用"){
							$(this).text("启用");
						}else{
							$(this).text("禁用");
						}
					})	
				}
		})
	}
	function fn(param,success,error){
		var comName=$('#comName').val(),
			orderNum=$('#orderNum').val(),
			sTime=$('#sTime').val(),
			eTime=$('#eTime').val();
		var obj={};
		if(comName!==''){
			obj.project_name=comName;
		}
		if(orderNum!==''){
			obj.id=orderNum;
		}
		if(sTime!==''){
			obj.starttime=sTime;
		}
		if(eTime!==''){
			obj.endtime=eTime;
		}
		console.log(obj);
		var url1 = 'https://apl.apluslabs.com/sudo/bills',
    　　　　ajax1 = $.ajax(
      　　 　　 {
         　　　　     url : url1,
         			type:'get',
					data: obj,
        　　　　}
 　　  　　 );
　　　　$.when(ajax1).done(function(e){
			console.log(e);
			var data=e.bills;
   　　　　 success(data);
   			qk();

　　　　}).fail(function(){
　　
   　　　　 alert("fail");
    
　　　　});
	}
function qk(){
	$('#comName').val(''),
	$('#orderNum').val('');
	$('#sTime').val('');
	$('#eTime').val('');
}
	
})
