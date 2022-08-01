new Vue({
    el:'#app',
    data:{
        account:'',
        password:""
    },
    methods:{
        submit(){
            if(this.account!=""&&this.password!=""){
                const url = `http://${config.ip}:8860/login`;
                const params = new URLSearchParams();
                params.append("numberP", this.account);
                params.append("password", this.password);
                axios.post(url,params).then(res=>{
                    console.log(res);
                    if(res.data.status==200){
                        window.location.href= `../student/look_data.html?studentId=${res.data.msg}`;
                    }else if(res.data.status==201){
                        popUp("密码错误","crimson");
                    }else if(res.data.status==202){
                        popUp("没有该账号","crimson");
                    }
                });
            }else{
                popUp("请输入信息","crimson");
            }
        },
        register(){
            window.location.href= '../student/studentIn.html';
        }
    }
})