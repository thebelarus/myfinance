function show_links_for_delete(){
    var elems = document.getElementsByName('delete_item')
    if(elems) {
        for(var i = 0;i < elems.length;i++) {
           if (elems[i].style.display != 'inline'){
                elems[i].style.display = 'inline'
           } else {
                // console.log(elems[i])
                elems[i].style.display = 'none'
           }
           //Do whatever else you need to do with the element.
        }
    }
}