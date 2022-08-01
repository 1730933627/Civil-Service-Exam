if(document.cookie.search("login=1") != -1){
    window.location.href= '../../html/admin/index.html'
} else{
    login = false;
}
$("#submin").click(()=>{
    let account = $("#account")[0].value
    let password = $("#password")[0].value
    if(account!==""&&password!==""){
        $.ajax({
            url : `http://${config.ip}:8860/login`,
            data: {
                account,
                password
            },
            type: "POST",
            dataType: "json",
            success(data){             
                if(data.status===200){
                    document.cookie="login=1;path=localhost";
                    document.cookie="login=1;path=127.0.0.1";
                    document.cookie=`permission=${data.msg};path=127.0.0.1`;
                    window.location.reload();
                }
                else if(data.status===201){
                    popUp("密码错误","crimson");
                }
                else if(data.status===202){
                    popUp("没有这个账号","crimson");
                }
            },
            error(error){
                console.log("出错了",error);
            }
        });
    }
    else{
        popUp("未输入完整数据","crimson");
    }
})