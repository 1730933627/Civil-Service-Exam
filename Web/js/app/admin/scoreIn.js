if(document.cookie.search("permission=0")!=-1){
}else if(document.cookie.search("permission=1")!=-1){
    window.location.href= '../../html/admin/student_manage.html';
}

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
if(GetRequest().studentId!=undefined){
    document.getElementById("studentId").value = GetRequest().studentId;
}
$("#submin").click(()=>{
    let studentId = $("#studentId").val();
    let score1 = $("#score1").val();
    let score2 = $("#score2").val();
    let score3 = $("#score3").val();
    if(studentId!==""&&score1!==""&&score2!==""&&score3!==""){
        let score = `['${score1}', '${score2}', '${score3}']`;
        const scoreList = [Number(score1),Number(score2),Number(score3)]
        let sumScore = eval(scoreList.join("+"))
        function scoreJudge(lists){
            for(let v of lists){
                if(v>100 || v<0)return false;
            }
            return true;
        }
        if(scoreJudge(scoreList)){
            $.ajax({
                url : `http://${config.ip}:8860/updateScore`,
                data: {
                    studentId,
                    score,
                    sumScore
                },
                type: "POST",
                dataType: "json",
                success(data){             
                    if(data.msg==="success"&&data.status===200){
                        popUp("发送成功","black")
                        $("#studentId")[0].value = "";
                        $("#score1")[0].value = "";
                        $("#score2")[0].value = "";
                        $("#score3")[0].value = "";
                    }
                    else if(data.status===201){
                        popUp("学号不存在","crimson");
                    }
                    else if(data.status===202){
                        popUp("未经允许的学生ID","crimson");
                    }
                },
                error(error){
                    popUp("出错了->error","red")
                    console.log("出错了->",error);
                }
            });
        }else{
            popUp("输入了错误的成绩","crimson");
        }
    }
    else{
        popUp("未输入完整数据","crimson");
    }
})