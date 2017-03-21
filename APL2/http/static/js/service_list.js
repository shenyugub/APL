$(function(){
	//渲染表格
	var url1 = 'https://apl.apluslabs.com/sudo/custom_service_items',
		url2 = 'https://apl.apluslabs.com/sudo/user_service_items',
    　　　　ajax1 = $.ajax(
      　　 　　 {
         　　　　   url : url1,
         			type:'get'
        　　　　}
 　　  　　 );
    		ajax2 = $.ajax(
    			{
    			 	url : url2,
         			type:'get'
    			}
    		)
    $.when(ajax1,ajax2).done(function(e1,e2){

    	console.log(e1);
    	console.log(e2);
    	var data1=e1[0].items,str='';
    	var data2=e2[0].items,str2='';
    	console.log(data1);
    	sta(data1);
    	sta(data2);
    	for(var i in data1){

    		str+='<tr>'
				+'<td>'
				+data1[i].id
				+'</td>'
				+'<td>'
				+'APL系统'
				+'</td>'
				+'<td>'
				+data1[i].title
				+'</td>'
				+'<td>'
				+data1[i].price
				+'</td>'
				+'<td>'
				+data1[i].status
				+'</td>'
				+'<td>'
				+data1[i].gmt_create
				+'</td>'
				+'</tr>';
    	}
    	$('.mainTab').find('tbody').append(str);
    	for(var i in data2){
    		str2+='<tr>'
				+'<td>'
				+data2[i].id
				+'</td>'
				+'<td>'
				+data2[i].project_name
				+'</td>'
				+'<td>'
				+data2[i].service_name
				+'</td>'
				+'<td>'
				+data2[i].price
				+'</td>'
				+'<td>'
				+data2[i].status
				+'</td>'
				+'<td>'
				+data2[i].gmt_create
				+'</td>'
				+'</tr>';
    	}
    	$('.mainTab').find('tbody').append(str2);
        var script=document.createElement('script');
        script.src='../../static/js/structure.js';
        document.body.appendChild(script);
    })
    function sta(datas){

    	for(var i in datas){
    		if(datas[i].status=='ServiceStatus.Submitting'){
    			datas[i].status='待提交';
            }else if(datas[i].status=='ServiceStatus.Submitted') {
                datas[i].status='已提交';
    		}else if(datas[i].status=='ServiceStatus.Ignoring'){
    			datas[i].status='请求忽略';
    		}else if(datas[i].status=='ServiceStatus.Ignored'){
    			datas[i].status='已忽略';
    		}else if(datas[i].status=='ServiceStatus.Rejected'){
    			datas[i].status='已驳回';
    		}else if(datas[i].status=='ServiceStatus.Verifying'){
    			datas[i].status='待审核';
    		}else if(datas[i].status=='ServiceStatus.Paying'){
    			datas[i].status='待支付';
    		}else if(datas[i].status=='ServiceStatus.Plannin'){
    			datas[i].status='待开发';
    		}else if(datas[i].status=='ServiceStatus.Developing'){
    			datas[i].status='开发中';
    		}else if(datas[i].status=='ServiceStatus.Finished'){
    			datas[i].status='开发完成';
    		}
    	}
    }
})