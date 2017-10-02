function go(id)
{
    var element = document.getElementById(id);
    if (element)
    {
        window.location = element.href;
        return true;
    }
    return false;
}

function toggleVisibility(element)
{
    if (element.style.display == "block")
    {
        element.style.display = "none";
    }
    else
    {
        element.style.display = "block";

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
            var exif = document.getElementById("exif");
            toggleVisibility(exif);
            document.cookie = "exif=" + exif.style.display + ";;path=/";
            break;

    }
};

var xDown = null;
var xUp = null;

function handleTouchStart(evt) {
    xDown = evt.touches[0].clientX;
};

function handleTouchMove(evt) {
    if (!xDown) return;
    xUp = evt.touches[0].clientX;
    var xDiff = xDown - xUp;

    if (Math.abs(xDiff) > 20) {
        var image = document.getElementById("image-itself");
        image.style.opacity = "0.6";
    }
}

function handleTouchEnd(evt) {
    if (!xDown || !xUp) return;
    var xDiff = xDown - xUp;

    if (Math.abs(xDiff) > 20) {/*most significant*/
        if ( xDiff > 0 ) {

            go("right") || go("home");
            /* left swipe */
        } else {
            go("left") || go("home");
            /* right swipe */
        }
    }
    else
    {
        var image = document.getElementById("image-itself");
        image.style.opacity = "1.0";
    }
    /* reset values */
    xDown = null;
    xUp = null;
}

document.addEventListener('touchstart', handleTouchStart, false);
document.addEventListener('touchmove', handleTouchMove, false);
document.addEventListener('touchend', handleTouchEnd, false);

if (document.cookie.split("; ").includes("exif=block"))
{
    document.getElementById("exif").style.display = "block";
}