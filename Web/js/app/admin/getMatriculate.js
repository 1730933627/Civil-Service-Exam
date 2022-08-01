new Vue({
    el: "#students",
    data:{
        matriculate:[],
    },
    methods:{
        getData(){
            const url = `http://${config.ip}:8860/getMatriculate`;
            axios.post(url).then((res) => {
                for(let v of res.data.data.matriculate){
                    v.allow="已录取";
                    v.allowColor="green";
                    v.fractions = "已过";
                    this.matriculate.push(v);
                }
                for(let v of res.data.data.unmatriculate){
                    v.allow="未录取";
                    v.allowColor="red";
                    v.conditionId = "无";
                    this.matriculate.push(v);
                }
            }).catch(function(err) {
                console.log(err);
            })
        }
    },
    beforeMount() {
        this.getData();
        console.log(this.matriculate)
    }
})
