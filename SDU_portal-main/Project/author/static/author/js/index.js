let edit = document.getElementsByClassName("edit")
let more = document.getElementById("more")
let more1 = document.getElementById("more1")

console.log(edit);
let isChecker = false;
let isText = false;
let isText1 = false;



  

function showEdit(item){
    console.log(item.getElementsByTagName("l")[0]);
    if(!isChecker){
    item.getElementsByTagName("l")[0].style.opacity="1"
    isChecker=true;
     }else{
        item.getElementsByTagName("l")[0].style.opacity="0";
         isChecker=false;
     }

}


function showMore(){
    if(!isText){
    more.innerText = "о подробнее."
    isText=true;
    }else{
        more.innerText="..."
        isText=false;
    }
}

function showMore1(){
    if(!isText1){
    more1.innerText = "о подробнее."
    isText1=true;
    }else{
        more1.innerText="..."
        isText1=false;
    }
}