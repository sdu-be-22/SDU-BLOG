$('.like-form').submit(function(e){
    e.preventDefault()
    var id = $(this).data('like')
    const _post_id=$('.like-btn-'+id).val();
    console.log(id)
     const url=$(this).attr('action') 
   $.ajax({
       method:"POST",
       url:url,

       data:{
        csrfmiddlewaretoken:"{{ csrf_token }}",
        post_id: _post_id,
       },
       success:function(response){
        if(response.lik===true){
            $('.like-icon-'+id).addClass('text-blue-700')
            $(".dislike-icon-"+id).removeClass("text-blue-700")
          }else{
            $('.like-icon-'+id).removeClass('text-blue-700')
          }
          
           like=$('#like-count-'+ id).text(response.likes_count)
           parseInt(like)
       },
       error:function(response){
        console.log("Failed ", response)
       }
   
    }) 
})



$('.dislike-form').submit(function(e){
    e.preventDefault()
    const id = $(this).data('dislike');
 
    const _post_id=$('.dislike-btn-' +id).val()
    const url =$(this).attr('action') 
      $.ajax({
           method:"POST",
           url:url, 
           data:{
            csrfmiddlewaretoken:"{{ csrf_token }}",
            post_id: _post_id,
           },
           
           success:function(response){
               if(response.dislikes ===true){
             
                   $(".dislike-icon-"+id).addClass("text-blue-700")
                   $('.like-icon-'+id).removeClass('text-blue-700')
               }else{
                   $(".dislike-icon-"+id).removeClass("text-blue-700")
                 
               }
           
               dislikes=$("#dislike-count-"+id).text(response.dislike_count)
               parseInt(dislikes)
               
           },
           error:function(response){
               console.log('failed', response.error)
           }
       }) 
    })
