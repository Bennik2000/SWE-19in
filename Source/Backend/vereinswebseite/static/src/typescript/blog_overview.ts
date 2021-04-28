let frontendHelper = new FrontendHelper()

function get_all_blogs(){

    let post_list = document.getElementById("post_list");
    function myOnloadFunction(response){
        
        if(response){

            if(response.success==true){
                
                response.blog_posts.forEach(post => {
                    function myOnloadFunction(response){

                        let col = document.createElement("div");
                        col.classList.add("col-md-12");
                        col.classList.add("mb-3");
    
                        let container = document.createElement("div");
                        container.classList.add("container");
                        container.classList.add("position-relative");
                        container.setAttribute("id","post");
    
                        let row = document.createElement("div");
                        row.classList.add("row");
    
                        let post_titel = document.createElement("h3");
                        post_titel.innerHTML=post.title;
                        post_titel.classList.add("col-sm-12");
                        post_titel.setAttribute("id","post_titel");
    
                        let post_meta = document.createElement("div");
                        post_meta.classList.add("col-sm-12");
                        post_meta.classList.add("mb-1");
                        post_meta.setAttribute("id","post_meta");
    
                        let post_author = document.createElement("span");
                        post_author.setAttribute("id","post_author");
                        post_author.innerHTML=post.author;
                        
                        let post_separator = document.createElement("hr");

                        let post_content = document.createElement("div");
                        post_content.classList.add("col-md-12");
                        post_content.setAttribute("id","post_content");
                        if(post.content.length>300){
                            post_content.innerHTML=response.html;
                        }
                        else{
                            post_content.innerHTML=response.html;
                        }
                        
                        let post_more = document.createElement("div");
                        post_more.classList.add("col-md-1");
                        post_more.classList.add("btn");
                        post_more.setAttribute("id","post_more");
                        post_more.setAttribute("href","#");
                        post_more.innerHTML = "mehr...";
                        post_meta.appendChild(post_author);
    
                        row.appendChild(post_titel);
                        row.appendChild(post_meta);
                        row.appendChild(post_separator);
                        row.appendChild(post_content);
                        row.appendChild(post_more);
                        container.appendChild(row);
                        col.appendChild(container);
    
                        post_list.appendChild(col);
                    }
                    let jsonObj ={};
                    jsonObj["content"]=post.content
                    
                    frontendHelper.makeHttpRequest("POST", "/blog_posts/render_preview", jsonObj, myOnloadFunction);
                    
                   


                });
                
            }else{
                alert("Server Error while loading Posts!");
            }
        }else{
            alert("Server Error while loading Posts!");
        }
        
    }
    let jsonObj ={};
    frontendHelper.makeHttpRequest("GET", "/blog_posts", jsonObj, myOnloadFunction);

}


window.onload=function(){
    get_all_blogs();
}