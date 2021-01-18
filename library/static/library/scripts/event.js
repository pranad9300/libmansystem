
document.addEventListener('click',event=>{
    
    const element = event.target;
    console.log(element.className);
    if (element.parentElement.className === "book-show"){
        
        
            
        if(element.innerHTML === "show_more"){
            
            element.parentElement.style = "height:500px;";
            let book_id = element.parentElement.querySelector('.showable-items');
            book_id.style = "display:initial";
          element.innerHTML = "show_less";
        }
        else{
            
            let book_id = element.parentElement.querySelector('.showable-items');
            book_id.style = "display:none;";
            element.parentElement.style = "height:400px;";
            element.innerHTML = "show_more";
        }
      
    }
   
});

document.addEventListener('DOMContentLoaded',()=>{
    
})
    
  
 