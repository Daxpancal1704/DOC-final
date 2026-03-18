document.addEventListener("DOMContentLoaded", function(){

console.log("History Page Loaded");

/* row animation */

let rows = document.querySelectorAll(".history-row");

rows.forEach((row,index)=>{

row.style.opacity = 0;
row.style.transform = "translateY(20px)";

setTimeout(()=>{

row.style.transition = "0.5s";
row.style.opacity = 1;
row.style.transform = "translateY(0)";

},index*120);

});

});