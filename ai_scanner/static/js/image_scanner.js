document.addEventListener("DOMContentLoaded", function(){

console.log("Image Scanner Loaded");

let bars = document.querySelectorAll(".progress-bar");

bars.forEach(bar => {

let value = bar.style.width;

bar.style.width = "0";

setTimeout(() => {
bar.style.width = value;
},300);

});

});