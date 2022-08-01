var list = new Object;
function GetRequest() {
    const url = location.search; //获取url中"?"符后的字串
    let theRequest = new Object();
    if (url.indexOf("?") != -1) {
        let str = url.substr(1);
        strs = str.split("&");
        for (let i = 0; i < strs.length; i++) {
            theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
        }
    }
    return theRequest;
}
window.onload = () => {
    let studentId = GetRequest().id;
    console.log(studentId);
    if (studentId !== "") {
        $.ajax({
            url: `http://${config.ip}:8860/matriculate`,
            data: {
                studentId,
            },
            type: "POST",
            dataType: "json",
            success(data) {
                if (data.status === 200) {
                    $("#table_student")[0].innerText = data.msg.studentId;
                    $("#table_name")[0].innerText = data.msg.name;
                    $("#table_profession")[0].innerText = data.msg.profession;
                    $("#table_sumScore")[0].innerText = data.msg.sumScore;
                    list['studentId'] = data.msg.studentId;
                    list['name'] = data.msg.name;
                    list['profession'] = data.msg.profession;
                    list['sumScore'] = data.msg.sumScore;
                    if (data.msg.conditionId === undefined) {
                        $("#table_condition")[0].innerText = "录取分数";
                        $("#table_conditionId")[0].innerText = data.msg.fractions;
                        list['fractions'] = data.msg.fractions;
                        $("#table_allow")[0].innerText = "未被录取";
                        $("#table_allow").css("color", "red");
                    } else {
                        $("#table_condition")[0].innerText = "录取公司ID";
                        $("#table_conditionId")[0].innerText = data.msg.conditionId;
                        list['conditionId'] = data.msg.conditionId;
                        $("#table_allow")[0].innerText = "已被录取";
                        $("#table_allow").css("color", "green");
                    }
                    $("#table").css("display", "block")
                }
                else if (data.status === 202) {
                    popUp("该学号不存在", "crimson");
                }
                else if (data.status === 203) {
                    popUp("请输入正确的学号", "crimson");
                }
            },
            error(error) {
                popUp("出错了->error", "red")
                console.log("出错了->", error);
            }
        });
    }
    else {
        popUp("未输入学号", "crimson");
    }
}
$("#download").click(() => {
    let url = `http://${config.ip}:8860/downloadPDF`;
    if (list["conditionId"] == undefined) {
        url += `?studentId=${list["studentId"]}&name=${list["name"]}&profession=${list["profession"]}&sumScore=${list["sumScore"]}&fractions=${list["fractions"]}`;
    } else {
        url += `?studentId=${list["studentId"]}&name=${list["name"]}&profession=${list["profession"]}&sumScore=${list["sumScore"]}&conditionId=${list["conditionId"]}`;
    }
    window.open(url, 'newwindow', `top=75,left=500,height=815,width=1000,location=no,newPage=${list["studentId"]},status=no,menubar=no,toolbar=no`);
})
