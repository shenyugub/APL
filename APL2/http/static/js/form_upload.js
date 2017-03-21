	function createXmlHttpRequest(){  
    		if(window.ActiveXObject){ //如果是IE浏览器  
        			return new ActiveXObject("Microsoft.XMLHTTP");  
    		}else if(window.XMLHttpRequest){ //非IE浏览器  
        			return new XMLHttpRequest();  
    		}  
	}
    
	var eleName;

	function uploadComplete(evt)
    {
        var obj = JSON.parse(evt.target.responseText).obj;

        if(obj)
        {
            var f = document.getElementsByName(eleName.id)[0];
            f.value = obj;

            alert('上传成功');
        }
        else
        {
            alert('上传失败');
        }
	}

	function uploadFailed(evt)
    {
		alert('上传失败');
	}

	function uploadFile(f)
    {
	    eleName=f;

        var url = 'https://apl-docs.oss-cn-beijing.aliyuncs.com';

        var file = document.getElementById(f.id).files[0];
        var k = file.name.substr(file.name.lastIndexOf('.'));
        var fd = new FormData();

        fd.append('OSSAccessKeyId', $('#OSSAccessKeyId').val());
        fd.append('x-oss-security-token', $('#x-oss-security-token').val());
        fd.append('policy', $('#policy').val());
        fd.append('Signature', $('#Signature').val());
        fd.append('key', guid() + k);
        fd.append("success_action_status", $('#success_action_status').val());
        fd.append("callback", $('#callback').val());
        fd.append("x:uid", document.getElementById('x:uid').value);
        fd.append("x:filename", file.name);
        fd.append("file", file);
        var xhr = createXmlHttpRequest();
        xhr.addEventListener("load", uploadComplete, false);
        xhr.addEventListener("error", uploadFailed, false);
        xhr.open('POST', url, true);
        xhr.send(fd);
    }


    function guid()
    {
        function S4()
        {
            return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
        }

        return (S4() + S4() + S4() + S4() + S4() + S4() + S4() + S4());
    }
