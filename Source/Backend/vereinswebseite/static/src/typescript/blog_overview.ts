let frontendHelper = new FrontendHelper()

function add_post_button(){
    window.location.href="/blog_posts/create"
}
function post_more_button(id:Number){
    window.location.href="/blog_posts/render?post_id="+id;
}
function post_edit_button(id:Number){
    window.location.href="/blog_posts/edit?post_id="+id;
}
function get_all_blogs(){

    let post_list = document.getElementById("post_list");

    function myOnloadFunctionPerosnal(responsePersonal){
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
                        
                        let post_date = document.createElement("span");
                        post_date.setAttribute("id","post_date");
                        post_date.innerHTML=post.creation_date;
    
                        let post_separator = document.createElement("hr");
    
                        let post_content = document.createElement("div");
                        post_content.classList.add("col-md-12");
                        post_content.setAttribute("id","post_content");
                      
                        post_content.innerHTML=response.html;
    
                        let post_more = document.createElement("div");
                        post_more.classList.add("col-md-1");
                        post_more.classList.add("btn");
                        post_more.setAttribute("onclick","post_more_button("+ post.id+");");
                        post_more.setAttribute("id","post_more");
                        post_more.setAttribute("href","#");
                        post_more.innerHTML = "mehr...";
                            
                            let post_edit = document.createElement("div");
                            post_edit.classList.add("col-md-1")
                            post_edit.classList.add("offset-md-10") 
                            post_edit.classList.add("btn");
                            post_edit.classList.add("btn-primary");
                            post_edit.classList.add("pl-2");
                            post_edit.setAttribute("onclick","post_edit_button("+post.id+");");
                            post_edit.setAttribute("id","post_edit");
                            post_edit.setAttribute("href","#");
                            post_edit.innerHTML = "bearbeiten";
                        
                        
    
                        post_meta.appendChild(post_author);
                        row.appendChild(post_titel);
                        row.appendChild(post_meta);
                        row.appendChild(post_separator);
                        row.appendChild(post_content);
                        row.appendChild(post_more);
                        if(responsePersonal.id==post.author_id){
                            row.appendChild(post_edit);
                        }
                        container.appendChild(row);
                        col.appendChild(container);
        
                        post_list.appendChild(col);
                    }
                    let jsonObj ={};
                    jsonObj["content"] = post.content;
                    frontendHelper.makeHttpRequest("POST", "/api/blog_posts/render_preview", jsonObj, myOnloadFunction);
    
                    });
                    
                }else{
                    alert("Server Error while loading Posts!");
                }
            }else{
                alert("Server Error!");
            }
            
        }
        let jsonObj ={};
        frontendHelper.makeHttpRequest("GET", "/api/blog_posts", jsonObj, myOnloadFunction);
    }

    let jsonObjPerosnal ={};
    frontendHelper.makeHttpRequest("GET", "/api/users/personal_info", jsonObjPerosnal, myOnloadFunctionPerosnal);

    

}


window.onload=function(){
    get_all_blogs();
}