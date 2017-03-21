$(function(){
function click(){
	if(event.button==2){
		alert("对不起,禁止使用此功能");
	}
}
document.onmousedown=click;
})
