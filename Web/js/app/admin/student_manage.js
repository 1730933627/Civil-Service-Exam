new Vue({
    el: "#students",
    data:{
        students:[],
        submitList:[],
        studentFilter:[],
        stuxg:[],
        findName:"",
        findId:"",
        sortText:"全部"
    },
    methods: {
        onChange(element) {
            if(element.target.checked){
                this.submitList.push(element.target.value)
                element.path[1].style.backgroundColor = "rgba(116, 185, 255,0.2)";
            }else{
                this.submitList.splice(this.submitList.indexOf(element.target.value),1)
                element.path[1].style.backgroundColor = "white";
            }
        },
        allowSubmit(){
            const url = `http://${config.ip}:8860/studentAllow`;
            if(this.submitList.length!==0){
                const params = new URLSearchParams();
                params.append("studentIds", this.submitList);
                axios.post(url,params).then(res => {
                    console.log(res)
                    this.getData();
                }).catch(function(err) {
                    console.log(err);
                })
                this.submitList = [];
            }
        },
        deleteSubmit(){
            if(confirm("确认删除吗?")){
                const url = `http://${config.ip}:8860/studentDelete`;
                if(this.submitList.length!==0){
                    const params = new URLSearchParams();
                    params.append("studentIds", this.submitList);
                    axios.post(url,params).then(res => {
                        console.log(res)
                        this.getData();
                    }).catch(function(err) {
                        console.log(err);
                    })
                    this.submitList = [];
                }
            }
        },
        getData(){
            const url = `http://${config.ip}:8860/getStudent`;
            this.students=[]
            axios.get(url).then(res => {
                for(let v of res.data.data){
                    if(v.sumScore==null){v.sumScore="空";}
                    if(v.allow === 0 || v.allow == undefined){
                        v.allow = "未允许";
                        v.allowColor = "red";
                    }else{
                        v.allow = "已允许";
                        v.allowColor = "green";
                    }
                    this.students.push(v)
                }
            }).catch(function(err) {
                console.log(err);
            })
            this.studentFilter = this.students;
        },
        getById(){
            if(this.findId !== ""){
                this.studentFilter = this.students.filter(p=>{
                    return String(p.studentId)===(this.findId)?p:undefined;
                });
            }else{
                this.studentFilter = this.students;
            }
        },
        modify(){
            if(this.submitList.length == 1){
                window.location.href= `../../html/admin/amend.html?studentId=${this.submitList[0]}`;
            }
            else if(this.submitList.length >= 2){
                window.alert("只能选择一个");
            }else{
                window.alert("请选择修改的学生");
            }
        },
        scoreIn(){
            if(document.cookie.search("permission=0")!=-1){
            }else if(document.cookie.search("permission=1")!=-1){
                alert("权限不足");
                return;
            }
            if(this.submitList.length == 1){
                window.open( `../../html/admin/scoreIn.html?studentId=${this.submitList[0]}`);
            }
            else if(this.submitList.length >= 2){
                window.alert("只能选择一个");
            }else{
                window.alert("请选择录入成绩的学生");
            }
        }
    },
    watch:{
        findName(){
            this.studentFilter = this.students.filter(p=>{
                return p.name.indexOf(this.findName) !== -1;
            });
        },
        sortText(){
            if(this.sortText=="全部"){
                this.studentFilter = this.students;
            }else{
                this.studentFilter = this.students.filter(p=>{
                    return p.profession.indexOf(this.sortText) !== -1;
                })
            };
        }
    },
    beforeMount(){
        this.getData();
    }
})
if(window.name != "bencalie"){
    location.reload();
    window.name = "bencalie";
    }else{
    window.name = "";
    }