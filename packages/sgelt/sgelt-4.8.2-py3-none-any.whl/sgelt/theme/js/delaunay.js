// From https://observablehq.com/@d3/hover-voronoi

const width = window.innerWidth;
const wHeight = window.innerHeight;

let div = document.getElementById("delaunay");
const dHeight = div.offsetHeight;  // div height
const size = width * dHeight;

// Limit Delaunay image size
const maxSize = 2000 * 3000;  // be reasonable
const maxHeight = maxSize / width;

// Limit parallax speed
const maxSpeed = 0.5;

var canvas = document.createElement("CANVAS");

// Canvas height is limited by maxHeight
canvas.height = Math.min(dHeight, maxHeight);
canvas.width = width;

// Compute scrolling heights
// foreground scroll height
const scrollHeight = Math.max(dHeight - wHeight, 0);  // zero if dHeight < wHeight
// background scroll height
const bgScrollHeight = canvas.height - wHeight;

// Speed is limited to stay inside background image
if (scrollHeight == 0) {
    var speed = maxSpeed;
} else {
    var speed = Math.min(bgScrollHeight / scrollHeight, maxSpeed);
}

var context = canvas.getContext('2d');
const n = canvas.height / 10;

Math.seed = 1;
// in order to work 'Math.seed' must NOT be undefined,
// so in any case, you HAVE to provide a Math.seed
Math.seededRandom = function () {
    Math.seed = (Math.seed * 9301 + 49297) % 233280;
    return Math.seed / 233280;
}

const particles = Array.from({ length: n }, () => [
    Math.seededRandom() * canvas.width,
    Math.seededRandom() * canvas.height,
]);

const delaunay = d3.Delaunay.from(particles);
const voronoi = delaunay.voronoi([0.5, 0.5, width - 0.5, canvas.height - 0.5]);
context.clearRect(0, 0, canvas.width, canvas.height);

context.beginPath();
voronoi.render(context);
voronoi.renderBounds(context);
context.strokeStyle = "lightgrey";
context.stroke();

$('#delaunay').parallax({ imageSrc: canvas.toDataURL("image/png"), speed: speed, positionY: "0px", naturalHeight: wHeight, bleed: 10});
$('img.parallax-slider').attr('alt', "image de fond : diagramme de Voronoi");
$('img.parallax-slider').attr('aria-hidden', "true");

