function GetRequest() {
    const url = location.search; //获取url中"?"符后的字串
    let theRequest = new Object();
    if (url.indexOf("?") != -1) {
       let str = url.substr(1);
       strs = str.split("&");
       for(let i = 0; i < strs.length; i ++) {
          theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
       }
    }
    return theRequest;
}
let oldStudentId = GetRequest().studentId;
new Vue({
    el:"#amend",
    data:{
        oldStudentId,
        person:{},
        params:Object
    },
    methods: {
        getPerson(){
            const url = `http://${config.ip}:8860/getPerson`;
            const params = new URLSearchParams();
            params.append("studentId", this.oldStudentId);
            axios.post(url,params).then(res => {
                const person = res.data.data[0];
                this.person = {
                    studentId:oldStudentId,
                    name:person.name,
                    sex:person.sex,
                    number:person.number,
                    profession:person.profession,
                    numberP:person.numberP,
                    education:person.education,
                    province:person.province
                }
            }).catch(err => {
                this.person = {
                    studentId:oldStudentId,
                    name:"",
                    sex:"男",
                    number:"",
                    profession:"NULL",
                    numberP:'NULL',
                    province:'NULL',
                    education:"NULL"
                }
            })
        },
        submit(){
            const url = `http://${config.ip}:8860/updatePerson`;
            const params = new URLSearchParams();
            params.append("oldStudentId", this.oldStudentId);
            params.append("studentId", this.person.studentId);
            params.append("name", this.person.name);
            params.append("sex", this.person.sex);
            params.append("number", this.person.number);
            params.append("profession", this.person.profession);
            params.append("numberP", this.person.numberP);
            params.append("education", this.person.education);
            params.append("province", this.person.province);
            console.log(this.person)
            axios.post(url,params).then(res => {
                console.log(res)
                if(res.data.status==200){
                    popUp("更改成功","black");
                }else if(res.data.status==201){
                    popUp("编号不可更改","crimson");
                }
            }).catch(err => {
                console.log(err)
                popUp("出错了","crimson");
            })
        }
    },
    beforeMount(){
        this.getPerson();
    }
})