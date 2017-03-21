$(function(){
	var locat=location.href,
		s=locat.indexOf("?"); 
		t=locat.substring(s+1);
		arr=t.split("=");
		uid=arr[1];
	$.ajax({
		url:'https://apl.apluslabs.com/sudo/projects/'+uid,
		type:'get',
		success:function(e){
			var data=e.project;
			console.log(data);
			//项目特点罗列
			//icon url
			var uid=data.icon_url;
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/file/'+uid,
				type:'get',
				success:function(e){
					$('.mes').find('.col-md-2').find('img').attr('src',e);
				},
				error:function(){
					alert("失败");
				}
			})
			//所属行业
			if(data.industry=='Industry.IntelligentMake'){
					data.industry='智能制造';
				}else if(data.industry=='Industry.IntelligentHardware'){
					data.industry='智能硬件';
				}else if(data.industry=='Industry.AI'){
					data.industry='人工智能';
				}else if(data.industry=='Industry.IoT'){
					data.industry='物联网';
				}else if(data.industry=='Industry.Sensor'){
					data.industry='传感器技术';
				}else if(data.industry=='Industry.NewMaterial'){
					data.industry='新材料新能源';
				}else if(data.industry=='Industry.ArVr'){
					data.industry='AR/VR';
				}else if(data.industry=='Industry.Drone'){
					data.industry='无人机';
				}else if(data.industry=='Industry.BigData'){
					data.industry='大数据';
				}else if(data.industry=='Industry.Medicine'){
					data.industry='医疗';
				}else if(data.industry=='Industry.Education'){
					data.industry='教育';
				}else if(data.industry=='Industry.Finance'){
					data.industry='金融';
				}else if(data.industry=='Industry.ConsumptionUpgrading'){
					data.industry='消费升级';
				}else if(data.industry=='Industry.O2O'){
					data.industry='O2O';
				}else if(data.industry=='Industry.BlackTechnology'){
					data.industry='黑科技';
				}else{
					data.industry='其他行业';
				}
			//公司阶段
			if(data.company_phase=='CompanyPhase.Seed'){
				data.company_phase='种子期';
			}else if(data.company_phase=='CompanyPhase.Initial'){
				data.company_phase='初创期';
			}else if(data.company_phase=='CompanyPhase.Growing'){
				data.company_phase='成长期';
			}else if(data.company_phase=='CompanyPhase.Extanding'){
				data.company_phase='扩张期';
			}else if(data.company_phase=='CompanyPhase.Mature'){
				data.company_phase='成熟期';
			}else if(data.company_phase=='CompanyPhase.PreIPOe'){
				data.company_phase='Pre-IPO';
			}

			var ids=data.phase_index;
			//title
			var title='';

			for(var i=0;i < data.phases.length;i++)
			{
				if(data.phases[i].phase_id == ids)
				{
                    title = data.phases[i].phase_name;
				}
			}

			$('.special').find('h5').text(title);
			var s='';
			s+='<span>'
				+'北京'
				+' | '
				+data.industry
				+' | '
				+data.company_phase
				+' | '
				+'2016-11-111'
				+'</span>';
			$('.mes').find('.col-md-10').find('p').prepend(s);
			//返回第一个表格
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/phases/'+ids,
				type:'get',
				success:function(e){
					console.log(e);
					var tabD=e.phase;
					var firTab=tabD.atts,
						t='';
					for(var i in firTab){
						t+='<tr><td>'
                         +firTab[i].name
                         +'</td><td>'
                         +firTab[i].description        
                         +'</td></tr>';
					}
					$('.mainTabs').find('tbody').html(t);
				},
				error:function(){
					alert("失败");
				}
			})
			//第二个表格
			var t='';
			t+='<tr><td>'
				+data.duration
				+'</td><td>' 
				+'2天'
				+'</td><td>'
				+'良好'
				+'</td></tr>'
			$('.tabt').find('tbody').html(t);
            //融资情况
            $('.financing').text(data.financing_status);	
            //项目点评
			var comments=data.comments,
				str='';
			console.log(comments);

			if(comments.length==0){
				$('#ly').css('display','block');
			}else{
				$('#ly').css('display','none');
			}
			for(var i in comments){
				str+='<p style="border-bottom:1px dashed #ccc">'
					+comments[i].content
					+'<span style="float:right;margin-right:3%">'
					+comments[i].gmt_create
					+'</span></p>';
			}
			$('.plBox').append(str);
			//项目概述
			//项目介绍
			$('.projects').find('.col-md-9').eq(0).text(data.description);
			//优势
			$('.projects').find('.col-md-9').eq(1).text(data.advantage);
			//交付日期
			$('.projects').find('.col-md-9').eq(2).text(data.deadline);
			//融资目标
			$('.projects').find('.col-md-9').eq(3).text(data.financing_sum+'万');
			//项目名称
			$('.mes').find('.col-md-10').find('h6').text(data.name);
			//商业计划书 bp_url <a class="btn btn-info" href="javascript:;">立即下载</a>
			var url=data.bp_url;
			$.ajax({
				url:'https://apl.apluslabs.com/sudo/file/'+url,
				type:'get',
				success:function(e){
					if(e){
						$('.projects').find('.col-md-9').eq(4).html('<a class="btn btn-info" href="'+e+'" download>立即下载</a>');
					}else{
						$('.projects').find('.col-md-9').eq(4).html('<a class="btn btn-info" disabled>未上传</a>');
					}
				},
				error:function(){
					alert("失败");
				}
			})
			//项目团队
			//联系人
			$('.proTeam').find('.col-md-9').eq(2).text(data.contact_name);
			//阶段
			var phases=data.phases,a='';
			for(var i in phases){
				a+='<div>'+phases[i].phase_name+'</div>';
			}
			$('.xmjd').html(a);
			//企业名称
			$('.proTeam').find('.col-md-9').eq(0).text(data.name);

		},
		error:function(){
			alert("失败");
		}
	})
	$('#tj').on('click',function(){
		var txt=$('#text').val();
		alert(txt);
	})
})