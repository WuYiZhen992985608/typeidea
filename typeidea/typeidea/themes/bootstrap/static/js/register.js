$(document).ready(function() {
    var account = document.getElementById('account')
    var pass = document.getElementById('pass')
    var passwd = document.getElementById('passwd')
    var accounterr = document.getElementById('accounterr')
    var checkerr = document.getElementById('checkerr')
    var passerr = document.getElementById('passerr')
    var passwderr = document.getElementById('passwderr')
    account.addEventListener('focus', function () {
        accounterr.style.display = 'none'
        checkerr.style.display = 'none'
    }, false)
    account.addEventListener('blur', function () {
        var inputStr = this.value
        if (inputStr.length < 8 || inputStr.length > 12) {
            accounterr.style.display = 'block'
            return
        }
        $.post("/checkuserid/0/", {'userid': inputStr}, function (data) {
            if (data.status == 'error') {
                checkerr.style.display = 'block'
            }
        })
    })
    // else{
    //     console.log('************')
    //     $.ajax({
    //         url:'/checkuserid/',
    //         type:'post',
    //         typedata:'json',
    //         data:{'checkid':account.value},
    //         success:function(data){
    //             console.log(data)
    //             if (data.status == 'error'){
    //                 checkerr.style.display = 'block'
    //             }
    //         }
    //     })
    // }
    // },false)
    pass.addEventListener('focus', function () {
        passerr.style.display = 'none'
    }, false)
    pass.addEventListener('blur', function () {
        var inputStr = this.value
        if (inputStr.length < 6 || inputStr.length > 16) {
            passerr.style.display = 'block'
        }
    }, false)
    passwd.addEventListener('focus', function () {
        passwderr.style.display = 'none'
    }, false)
    passwd.addEventListener('blur', function () {
        var inputStr = this.value
        if (inputStr != pass.value) {
            passwderr.style.display = 'block'
        }
    }, false)
})