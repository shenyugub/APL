$(function(){
	$('.card').on('click',function(){
		$('.mark').show();
		$('#tck').show();
	})
	//渲染数据
	$('#tt').datagrid({
				loader:fn,
				singleSelect: true,
				nowrap:false,
				loadMsg: '数据加载中.....',
				frozenColumns:[[
					{field:'id',title:'编号',align:'center',width:'10%'},
					{field:'title',title:'服务项名称',align:'center',width:'25%'},
				]],
				columns:[[
					{field:'description',title:'服务项描述',align:'center',width:'40%'},
					{field:'category_name',title:'类别',align:'center',width:'16%'},
					{field:'price',title:'报价',align:'center',width:'11%'}
				]],
				onLoadSuccess:function(){
					var script=document.createElement('script');
					script.src='../../static/js/structure.js';
					document.body.appendChild(script);						
				}
		})
	function fn(param,success,error){
		var url1 = 'https://apl.apluslabs.com/sudo/custom_service_items',
   　　 　　
    　　　　ajax1 = $.ajax(
      　　 　　 {
         　　　　     url : url1,
					type:'get',
                	dataType: 'json'
        　　　　}
 　　  　　 );
　　　　$.when(ajax1).done(function(e){
			var data=e.items;
			success(data);
		console.log(e)
　　　　}).fail(function(){
　　
   　　　　 alert("fail");
    
　　　　});
	}
	
	
})