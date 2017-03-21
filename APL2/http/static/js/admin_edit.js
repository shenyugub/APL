$(function(){
	//截取id
	var locat=location.href,
		s=locat.indexOf("?"); 
		t=locat.substring(s+1);
		arr=t.split("=");
		uid=arr[1];
	$.ajax({
		url:'https://apl.apluslabs.com/sudo/users/'+uid,
		type:'get',
        success:function(e){
        	console.log(e);
        	var datas=e.user;
        	//角色
        	var type=datas.type;
        	if(type=='UserType.Startup'){
        		$('#roles option:eq(0)').attr('selected','selected');
        		$('.tabQ').eq(0).css('display','block').siblings('.tabQ').css('display','none');
        		//企业名称
        		var company_name=datas.company_name;
        		$('#company_name').val(company_name);
        		//企业简介
        		var company_desc=datas.company_desc;
        		$('#company_desc').val(company_desc);
        		//所属行业
        		var company_industry=datas.company_industry,
        			c=company_industry.substr(9);
        		var options=$('#company_industry').find('option').splice(0,16);
        		for(var i in options){
        			if(c==$(options[i]).val()){
        				$('#company_industry option:eq('+i+')').attr('selected','selected');
        			}
        		}
        	}else{
        		$('#roles option:eq(1)').attr('selected','selected');
        		$('.tabQ').eq(1).css('display','block').siblings('.tabQ').css('display','none');
        		//关注的领域
        		var interested=datas.interested.split(',');
        		var cks=$(document.getElementsByName('ck')).splice(0,16);
        		console.log(cks)
        		for(var i in interested){
        			for(var j in cks){
        				/*console.log($(cks[j]).val());*/
        				if(interested[i]==$(cks[j]).val()){
        					$(document.getElementsByName('ck')).eq(j).prop('checked',true);
        				}
        			}
        		}
        		//投资身份
        		var invest_role=datas.invest_role;
        		if(invest_role=='InvestmentType.Organization'){
        			$('#invest_role option:eq(2)').attr('selected','selected');
        		}else if(invest_role=='InvestmentType.Individual'){
        			$('#invest_role option:eq(1)').attr('selected','selected');
        		}
        		//最小额度
        		var investment_min=datas.investment_min;
        		$('#investment_min').val(investment_min);
        		//最大额度
        		var investment_max=datas.investment_max;
        		$('#investment_max').val(investment_max);
        		//投资阶段
        		var invest_phase=datas.invest_phase.split(',');
        		var cks1=$(document.getElementsByName('ck1')).splice(0,16);
        		console.log(cks)
        		for(var i in invest_phase){
        			for(var j in cks1){
        				/*console.log($(cks[j]).val());*/
        				if(invest_phase[i]==$(cks1[j]).val()){
        					$(document.getElementsByName('ck1')).eq(j).prop('checked',true);
        				}
        			}
        		}
        	}
        	//姓名
        	var name=datas.name;
        	$('#name').val(name);
        	//邮箱
        	var email=datas.email;
        	$('#email').val(email);
        	//手机号
        	var phone=datas.phone;
        	$('#phone').val(phone);
        	//微信号
        	var wechat=datas.wechat;
        	$('#wechat').val(wechat);
        	//职位
        	var company=datas.company;
        	$('#company').val(company);
        	//性别
        	var sex=datas.gender;
        	if(sex=='Gender.Male'){
        		$('#optionsRadios3').prop('checked',true);
        	}else{
        		$('#optionsRadios4').prop('checked',true);
        	}
        	//个人简介
        	var resume=datas.resume;
        	$('#resume').val(resume);
        	var id=datas.id;
        	xg(id);
        	
        },
        error:function(){
        	alert("失败");
        }
	})
	//点击修改
function xg(ids){
	var obj={};
	$('#ktzh').on('click',function(){
		var name=$('#name').val(),
			email=$('#email').val(),
			phone=$('#phone').val(),
			wechat=$('#wechat').val(),
			company=$('#company').val(),
			resume=$('#resume').val(),
			company_name=$('#company_name').val(),
			company_desc=$('#company_desc').val(),
			company_industry=$('#company_industry option:selected').val(),
			invest_role=$('#invest_role option:selected').val(),
			investment_min=$('#investment_min').val(),
			investment_max=$('#investment_max').val(),
			type=$('#roles option:selected').text();
		//公共
		var sex=$(':radio:checked').val();
		obj.gender=sex;
		if(name!==''){
			obj.name=name;
		}else{
			if(obj.name){
				delete obj.name; 
			}
		}
		if(email!==''){
			obj.email=email;
		}else{
			if(obj.email){
				delete obj.email; 
			}
		}
		if(phone!==''){
			obj.phone=phone;
		}else{
			if(obj.phone){
				delete obj.phone; 
			}
		}
		if(wechat!==''){
			obj.wechat=wechat;
		}else{
			if(obj.wechat){
				delete obj.wechat; 
			}
		}
		if(company!==''){
			obj.company=company;
		}else{
			if(obj.company){
				delete obj.company; 
			}
		}
		if(resume!==''){
			obj.resume=resume;
		}else{
			if(obj.resume){
				delete obj.resume; 
			}
		}
		if(type=='项目方'){
			obj.type='Startup';
			if(obj.invest_role){
				delete obj.invest_role;
			}
			if(obj.investment_min){
				delete obj.investment_min;
			}
			if(obj.investment_max){
				delete obj.investment_max;
			}
			if(obj.interested){
				delete obj.interested;
			}
			if(obj.invest_phase){
				delete obj.invest_phase;
			}

			if(company_name!==''){
				obj.company_name=company_name;
			}
			if(company_desc!==''){
				obj.company_desc=company_desc;
			}
			if(company_industry!=='请选择'){
				obj.company_industry=company_industry;
			}

		}else{
			obj.type='Investor';
			if(obj.company_name){
				delete obj.company_name;
			}
			if(obj.company_desc){
				delete obj.company_desc;
			}
			if(obj.company_industry){
				delete obj.company_industry;
			}
			if(invest_role!=='请选择'){
				obj.invest_role=invest_role;
			}
			if(investment_min!==''){
				obj.investment_min=investment_min;
			}
			if(investment_max!==''){
				obj.investment_max=investment_max;
			}
			text = $("input:checkbox[name='ck']:checked").map(function(index,elem) {
            		return $(elem).val();
       			 }).get().join(',');
			if(text!==''){
				obj.interested=text;
			}
			invest_phase = $("input:checkbox[name='ck1']:checked").map(function(index,elem) {
            		return $(elem).val();
       			 }).get().join(',');
			if(invest_phase!==''){
				obj.interested=invest_phase;
			}
		}
		console.log(obj);
		ajaxData(obj,ids)
	})
	}
	
	function ajaxData(obj,uid){
		$.ajax({
			url:'https://apl.apluslabs.com/sudo/users/'+uid,
			data: JSON.stringify(obj),
			type:'post',
            dataType: 'json',
            contentType:'application/json',
			success:function(e){
				console.log(e);
				location.href='./admin_list.html';
			},
			error:function(){
				alert('获取数据失败');
			}
		})
	} 

})