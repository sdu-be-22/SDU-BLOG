function addFav(id,user_id){
    axios.get(base_url+"/api/fav/add.php?id="+id+"&user_id="+user_id).then(res=>{
         console.log(res.data);
    });
}