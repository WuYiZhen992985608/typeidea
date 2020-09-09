$(document).ready(function(){
    console.log('+_+_+_++_');
    collectfavorite();
});
function collectfavorite() {
        var collect_a = document.getElementById("collect");
        collect_a.addEventListener("click", function () {
            var blogid = this.getAttribute("class");
            console.log('+_+_+_++_');
            console.log(blogid);
            $.get('/changefavorite/{{ blogid }}/', function (data) {
                if (data.status == 'success') {
                    console.log(data.title);
                    document.getElementById('collect').innerHTML = '已收藏';
                } else {
                    if (data.data == -1) {
                        window.location.href = "{% url 'post-detail' blogid %}";
                    }
                }
            })
        }, false);
    };