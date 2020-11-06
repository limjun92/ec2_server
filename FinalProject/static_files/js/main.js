function modal_open() {
    document.getElementById("modal").style.display = "block";
}
function modal_close() {
    document.getElementById("modal").style.display = "none";
}


var fileName;
$("#file").on('change',function(){
    fileName = $("#file").val();
    if(fileName != null) {
        $('#submit').css('color', '#E16350');
    }
});

$("#submit").on('click',function() {
    if(fileName != null) {
        setTimeout(function(){
            $('#submit').attr('type', 'submit');
            $('#submit').trigger("click");
            console.log("test");
        }, 3000);

        $("#title").css('display', 'none');
        $("#modal_open").css('display', 'none');
        $("#modal").css('display', 'none');
        $("#loading").css('display', 'block');
    }
});



TweenMax.set('#circlePath', {
    attr: {
    r: document.querySelector('#mainCircle').getAttribute('r')
    }
})
MorphSVGPlugin.convertToPath('#circlePath');

var xmlns = "http://www.w3.org/2000/svg",
    xlinkns = "http://www.w3.org/1999/xlink",
    select = function(s) {
    return document.querySelector(s);
    },
    selectAll = function(s) {
    return document.querySelectorAll(s);
    },
    mainCircle = select('#mainCircle'),
    mainContainer = select('#mainContainer'),
    car = select('#car'),
    mainSVG = select('.mainSVG'),
    mainCircleRadius = Number(mainCircle.getAttribute('r')),
    //radius = mainCircleRadius,
    numDots = mainCircleRadius / 2,
    step = 360 / numDots,
    dotMin = 0,
    circlePath = select('#circlePath')

//
//mainSVG.appendChild(circlePath);
TweenMax.set('svg', {
    visibility: 'visible'
})
TweenMax.set([car], {
    transformOrigin: '50% 50%'
})
TweenMax.set('#carRot', {
    transformOrigin: '0% 0%',
    rotation:30
})

var circleBezier = MorphSVGPlugin.pathDataToBezier(circlePath.getAttribute('d'), {
    offsetX: -20,
    offsetY: -5
})



//console.log(circlePath)
var mainTl = new TimelineMax();

function makeDots() {
    var d, angle, tl;
    for (var i = 0; i < numDots; i++) {

    d = select('#puff').cloneNode(true);
    mainContainer.appendChild(d);
    angle = step * i;
    TweenMax.set(d, {
        //attr: {
        x: (Math.cos(angle * Math.PI / 180) * mainCircleRadius) + 400,
        y: (Math.sin(angle * Math.PI / 180) * mainCircleRadius) + 300,
        rotation: Math.random() * 360,
        transformOrigin: '50% 50%'
        //}
    })

    tl = new TimelineMax({
        repeat: -1
    });
    tl
        .from(d, 0.2, {
        scale: 0,
        ease: Power4.easeIn
        })
        .to(d, 1.8, {
        scale: Math.random() + 2,
        alpha: 0,
        ease: Power4.easeOut
        })

    mainTl.add(tl, i / (numDots / tl.duration()))
    }
    var carTl = new TimelineMax({
    repeat: -1
    });
    carTl.to(car, tl.duration(), {
    bezier: {
        type: "cubic",
        values: circleBezier,
        autoRotate: true
    },
    ease: Linear.easeNone
    })
    mainTl.add(carTl, 0.1)
}

makeDots();
mainTl.time(120);
TweenMax.to(mainContainer, 20, {
    rotation: -360,
    svgOrigin: '400 300',
    repeat: -1,
    ease: Linear.easeNone
});
mainTl.timeScale(0.8)