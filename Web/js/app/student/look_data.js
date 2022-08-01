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
let studnetId = GetRequest().studentId;
new Vue({
    el:"#root",
    data:{
        datas:{},
        allow:false
    },
    methods:{
        getDatas(){
            const url = `http://${config.ip}:8860/getPerson`;
            const params = new URLSearchParams();
            params.append("studentId", studnetId);
            axios.post(url,params).then(res => {
                console.log(res)
                const person = res.data.data[0];
                if(person.allow===1){
                    this.allow = true;
                }
                this.datas={
                    studentId:person.studentId,
                    name:person.name,
                    sex:person.sex,
                    number:person.number,
                    profession:person.profession,
                    date:person.date
                }
            }).catch(err => {
                this.datas={
                    studentId:studnetId,
                    name:"",
                    sex:"男",
                    number:"",
                    profession:"NULL",
                    date:"0000-00-00"
                }
            })
        },
        download(){
            let url = `http://${config.ip}:8860/downloadPDF`;
            url += `?studentId=${this.datas.studentId}&method='准考证'`;
            window.open(url, 'newwindow', `top=75,left=500,height=1000,width=1000,location=no,newPage=${this.datas.studentId},status=no,menubar=no,toolbar=no`);
        }
    },
    beforeMount(){
        this.getDatas();
    },
})