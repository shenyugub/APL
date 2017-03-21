$(function(){
	ajaxs();
	//弹出框数据清空
	function zero(){
		$('#serName').val('');
		$('#serDec').val('');
		$('#prices').val('');
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
				url:'https://apl.apluslabs.com/sudo/service_categories',
				type:'get',
           		dataType: 'json',
            	success:function(e){
            		var data=e.service_category_list;
            			arr=[],
            			s='';
            		for(var i in data){
            			s+='<option value='+data[i].id+'>'+data[i].name+'</option>';
            		}
            		$('#sorts').html(s);
            	},
            	error:function(){
            		alert("失败");
            	}
            })
		getData();
	})
	//点击弹出框内的内容，获取值
	function getData(){
		var obj={};
		$('.confirmBtn').unbind('click').click(function(){
			var category=$('#sorts option:selected').val(),
				serName=$('#serName').val(),
				serDec=$('#serDec').val(),
				prices=$('#prices').val();
				obj.category_id=category;
				obj.name=serName;
				obj.desc=serDec;
				obj.price=prices;
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/service_items',
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
	
	//渲染数据
	function ajaxs(){
		$('#tt').datagrid({
				loader:fn,
				singleSelect: true,
				nowrap:false,
				loadMsg: '数据加载中.....',
				frozenColumns:[[
					{field:'id',title:'编号',align:'center',width:'10%'},
					{field:'name',title:'服务项名称',align:'center',width:'25%'},
				]],
				columns:[[
					{field:'desc',title:'服务项描述',align:'center',width:'40%'},
					{field:'category_name',title:'类别',align:'center',width:'16%'},
					{field:'price',title:'报价',align:'center',width:'16%'}
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
				/*onClickCell: function (index,field,value) {
					if (field == 'cz') {
						$('.dis').eq(index).text("启用")
					}
				}*/
		})
	}
	
function fn(param,success,error){
	var url1 = 'https://apl.apluslabs.com/sudo/service_items',　
    ajax1 = $.ajax(
      　　  	{
         　　　　   url : url1,
					type:'get',
           			dataType: 'json'
        　　　　}
 　　  　　 );

　　　　$.when(ajax1).done(function(e){
			var data=e.service_item_list;
   　　　　	success(data);

　　　　}).fail(function(){
　　
   　　　　 alert("fail");
    
　　　　});
}
	
	
})