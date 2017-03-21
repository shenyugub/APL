$(function(){
	window.API_HOST = (function(){
  		return {
     		'apl.apluslabs.com':'apl.apluslabs.com',
      		'172.16.46.53:5000':'172.16.46.53:5000'
    		}[window.location.host] || window.location.host
	})();
	console.log(window.location.host);
	if(window.API_HOST=='localhost'){
		window.API_HOST='172.16.46.53:5000'
	}
	var url = '//'+window.API_HOST + '/sudo/users';
	console.log(url);
	tabData();
	//切换角色
	$('#identity').on('change',function(){
		var identity=$('#identity option:selected').text();
		$("#industry option:first").prop("selected", true);
		$('#comName').val('');
		if(identity=='投资人'){
			$('.hy').css('display','none');
			$('.mc').css('display','none');
			$('.an').css('margin-top',-2+'%');
		}else{
			$('.hy').css('display','block');
			$('.mc').css('display','block');
			$('.an').css('margin-top',0);
		}
	})
	
	//点击查询获取数据
	$('#search').on('click',function(){
		tabData();
	})
	//渲染表格数据
	function tabData(){
		$('#tt').datagrid({
				loader:fn,
				//url:'https://apl.apluslabs.com/sudo/users',
				//url:url,
				singleSelect: true,
				loadMsg: '数据加载中.....',				
				//pageSize:10,
				//pageList:[10,20,50],
				//pagination:true,
				nowrap:false,
				frozenColumns:[[
					{field:'id',title:'会员编号',align:'center'},
					{field:'name',title:'会员名称',align:'center'},
				]],
				columns:[[
					{field:'email',title:'邮箱账号',align:'center'},
					{field:'phone',title:'手机号',align:'center'},
					{field:'wechat',title:'微信账号',align:'center'},
					{field:'company',title:'公司及职位',align:'center'},
					{field:'gender',title:'性别',align:'center'},
					{field:'company_name',title:'企业名称',align:'center'},
					{field:'company_industry',title:'所属行业',align:'center'},
					{field:'invest_role',title:'投资身份',align:'center'},
					{field:'register_time',title:'注册日期',align:'center'},
					{field:'cz',align:'center',width:'100px',title:'操作',
						formatter: function (vales ,row, index ) {
							var bh=row.id;
							var a = '<a class="dis" id="'+bh+'"></a> <a class="amend" data_id="'+bh+'">修改</a>';
							return a;
						}
					}
				]],
				onLoadSuccess:function(data){
					var script=document.createElement('script');
					script.src='../../static/js/structure.js';
					document.body.appendChild(script);
					for(var i in data.rows){
						if(data.rows[i].active==true){
							$($('.dis')[i]).text('启用');
							
						}else{
							$($('.dis')[i]).text('禁用');
							
						}
					}
					$('.dis').on('click',function(){
						if($(this).text()=="禁用"){
							$(this).text("启用");
						}else{
							$(this).text("禁用");
						}
						var uid=$(this).attr('id'),
							aObj={};
						if($(this).text()=='启用'){
							aObj.active=1;
						}else{
							aObj.active=0;
						}
						$.ajax({
							url:'https://apl.apluslabs.com/sudo/users/'+uid,
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
					})	
					$('.amend').on('click',function(){
						var uid=$(this).attr('data_id');
						location.href='./admin_edit.html?uid='+uid;
					})
				}
		})
	}
	function fn(param,success,error){
		var serialNum=$('#serialNum').val(),
			names=$('#names').val(),
			account=$('#account').val(),
			comName=$('#comName').val(),
			identity=$('#identity option:selected').val(),
			industry=$('#industry option:selected').val(),
			tele=$('#tele').val();
		var obj={};
		if(serialNum!==''){
			obj.id=serialNum;
		}
		if(names!==''){
			obj.name=names;
		}
		if(account!==''){
			obj.email=account;
		}
		if(tele!==''){
			obj.phone=tele;
		}
		if(comName!==''){
			obj.company_name=comName;
		}
		if(identity!=='请选择'){
			obj.type=identity;
		}
		if(industry!=='请选择'){
			obj.company_industry=industry;
		}
		console.log(obj);
		//var url1 = 'https://apl.apluslabs.com/sudo/users',
		//var url1 = 'http://172.16.46.53:5000/sudo/users',
		var url1 = url,
    　　　　ajax1 = $.ajax(
      　　 　　 {
         　　　　   url : url1,
         			type:'get',
         			data: obj
        　　　　}
 　　  　　 );

　　　　$.when(ajax1).done(function(e){
			var data=e.users;
			console.log(data);
			for(var i in data){
				if(data[i].gender=='Gender.Female'){
					data[i].gender='女';
				}else{
					data[i].gender='男';
				}
				if(data[i].invest_role=='InvestmentType.Individual'){
					data[i].invest_role='个人';
				}else{
					data[i].invest_role='机构';
				}
				if(data[i].company_industry=='Industry.IntelligentMake'){
					data[i].company_industry='智能制造';
				}else if(data[i].company_industry=='Industry.IntelligentHardware'){
					data[i].company_industry='智能硬件';
				}else if(data[i].company_industry=='Industry.AI'){
					data[i].company_industry='人工智能';
				}else if(data[i].company_industry=='Industry.IoT'){
					data[i].company_industry='物联网';
				}else if(data[i].company_industry=='Industry.Sensor'){
					data[i].company_industry='传感器技术';
				}else if(data[i].company_industry=='Industry.NewMaterial'){
					data[i].company_industry='新材料新能源';
				}else if(data[i].company_industry=='Industry.ArVr'){
					data[i].company_industry='AR/VR';
				}else if(data[i].company_industry=='Industry.Drone'){
					data[i].company_industry='无人机';
				}else if(data[i].company_industry=='Industry.BigData'){
					data[i].company_industry='大数据';
				}else if(data[i].company_industry=='Industry.Medicine'){
					data[i].company_industry='医疗';
				}else if(data[i].company_industry=='Industry.Education'){
					data[i].company_industry='教育';
				}else if(data[i].company_industry=='Industry.Finance'){
					data[i].company_industry='金融';
				}else if(data[i].company_industry=='Industry.ConsumptionUpgrading'){
					data[i].company_industry='消费升级';
				}else if(data[i].company_industry=='Industry.O2O'){
					data[i].company_industry='O2O';
				}else if(data[i].company_industry=='Industry.BlackTechnology'){
					data[i].company_industry='黑科技';
				}else{
					data[i].company_industry='其他';
				}

			}
			success(data);
			qk();
			

　　　　}).fail(function(){
　　
   　　　　 alert("fail");
    
　　　　});
}
function qk(){
	$('#serialNum').val(''),
	$('#names').val('');
	$('#account').val('');
	$('#comName').val('');
	$('#tele').val('');
}
	
})
