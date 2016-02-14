function go(id)
{
    var element = document.getElementById(id);
    if (element)
    {
        window.location = element.href;
    }
}

document.onkeydown = function(evt) {
    evt = evt || window.event;
    switch (evt.keyCode) {
        case 33: //pgup
        case 37: //left
        case 38: //up
        case 8:  //backspace
            go("left");
            break;
        case 32: //space
        case 13: //enter
        case 34: //pgdn
        case 39: //right
        case 40: //down
            go("right");
            break;
        case 36: //home
        case 27: //esc
            go("home");
            break;
        case 73: // i
            //reserved
            break;
    }
};

// TODO: Add swipe
