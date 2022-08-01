new Vue({
    el:'#app',
    data:{
        number:'',
        numberP:''
    },
    methods:{
        submit(){
            const url = `http://${config.ip}:8860/byPhone`;
            const params = new URLSearchParams();
            params.append("number", this.number);
            params.append("numberP", this.numberP);
            axios.post(url,params).then(res=>{
                if(res.data.status==200){
                    popUp(`密码为:${res.data.data.data[0].password}`,"black");
                    console.log(res.data.data.data[0].password)
                }else if(res.data.status==201){
                    popUp("没有该学生","crimson");
                }
            });
        }
    }
})