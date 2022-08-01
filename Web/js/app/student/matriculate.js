$("#submin").click(()=>{
    let studentId = $("#studentId").val();
    if(studentId!==""){
        $.ajax({
            url : `http://${config.ip}:8860/matriculate`,
            data: {
                studentId,
            },
            type: "POST",
            dataType: "json",
            success(data){  
                // console.log(studentId)           
                if(data.status===200){
                    window.location.href=`student_s.html?id=${data.msg.studentId}`;
                }
                else if(data.status===201){
                    popUp("学生没有成绩","crimson")
                }
                else if(data.status===202){
                    popUp("该学号不存在","crimson");
                }
                else if(data.status===203){
                    popUp("请输入正确的学号","crimson");
                }
            },
            error(error){
                popUp("出错了->error","red")
                console.log("出错了->",error);
            }
        });
    }
    else{
        popUp("未输入学号","crimson");
    }
})