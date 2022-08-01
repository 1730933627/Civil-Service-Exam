new Vue({
    el:"#center",
    data:{
        studentId:"",
        name:"",
        sex:"男",
        number:"",
        birthday:"",
        province:"",
        numberP:"",
        password:"",
        profession:"NULL",
        education:"NULL",
        password1:''
    },
    methods: {
        setId(professions=this.profession){
            const now = new Date()
            let studentId = new Date().getTime();            
            y = String(now.getFullYear()).slice(2,4),
            m = String(now.getMonth() + 1).length==1?"0"+String(now.getMonth() + 1):String(now.getMonth() + 1);

            if(professions == "法律"){
                studentId =  y+"179"+ m +parseInt(studentId%10000);
            }
            else if(professions == "行政"){
                studentId = y+"178"+ m +parseInt(studentId%10000);
            }
            else if(professions == "财经"){
                studentId = y+"177"+ m +parseInt(studentId%10000);
            }else{
                popUp("请选择专业","crimson");
            }
            return studentId
        },
        submit(){
            this.studentId = this.setId();
            if(this.studentId!=""&&this.name!=""&&this.number!=""&&this.birthday!=""&&this.province!=""&&this.numberP!=""&&this.password!=""&&this.profession!="NULL"&&this.education!="NULL"){
                
            }
            if(this.password != this.password1){
                popUp("密码和确认密码不一致");
                return
            }
            if(this.number.length!=18){
                popUp("身份证号码无效","crimson");
                return;
            }
            if(this.studentId!=""&&this.name!=""&&this.number!=""&&this.birthday!=""&&this.province!=""&&this.numberP!=""&&this.password!=""&&this.profession!="NULL"&&this.education!="NULL"){
                const params = new URLSearchParams();
                params.append("studentId", this.studentId);
                params.append("name", this.name);
                params.append("sex", this.sex);
                params.append("number", this.number);
                params.append("birthday", this.birthday);
                params.append("province", this.province);
                params.append("numberP", this.numberP);
                params.append("password", this.password);
                params.append("profession", this.profession);
                params.append("education", this.education);
                axios.post(`http://${config.ip}:8860/insertStudent`,params).then(res=>{
                    if(res.data.msg==="success"&&res.data.status===200){
                        popUp("成功录入","black");
                        setTimeout(()=>{
                            window.location.href = `../../html/student/look_data.html?studentId=${this.studentId}`;
                        },1000);
                    }
                    else if(res.data.status===201){
                        popUp("身份证号已注册","crimson");
                    }
                    else if(res.data.status==202){
                        popUp("信息不能为空","crimson")
                    }
                    else if(res.data.status==203){
                        popUp("注册时间已过","crimson")
                    }
                    else if(res.data.status==204){
                        popUp("注册还没开始","crimson")
                    }else if(res.data.status==205){
                        popUp("电话号已存在","crimson")
                    }
                });
            }else{
                popUp("信息不能为空","crimson")
            }
        }
    },  
})
