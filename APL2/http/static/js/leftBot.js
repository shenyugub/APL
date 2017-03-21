$(function(){
	$('.ul').find('li').on('click',function(){
		$(this).next('ol').toggle();
	})
	$('.dis').on('click',function(){
		console.log($(this).parents('td').siblings('td').text())
	})
})