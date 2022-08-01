function popUp(text="",color="black"){
    try{
        $("#pops")[0].childNodes[0].remove()
    }
    catch{}
    const temp = $('<div></div>');
    temp.text(text);
    temp.css("color",color)
    temp.attr('id','popUp');
    temp.addClass('popUp');
    temp.appendTo($("#pops"));
}