$("#submin").click(()=>{
    let name = $("#name").val();
    let number = $("#number").val();
    if(name!=""&&number!=""){
        $.ajax({
            url : `http://${config.ip}:8860/byPhone`,
            data: {
                name,
                number
            },
            type: "POST",
            dataType: "json",
            success(data){
                if(data.status===200){
                    window.location.href = `../../html/student/look_data.html?studentId=${data.data.data[0].studentId}`;
                }else if(data.status===201){
                    popUp("没有该学生","crimson")
                }
            },
            error(error){
                popUp("出错了->error","red")
                console.log("出错了->",error);
            }
        });
    }else{
        popUp("请输入数据","crimson");
    }
})