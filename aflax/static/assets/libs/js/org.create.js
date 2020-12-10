// Recommended Products
$(document).ready(function(){
    $.ajax({
        url: 'indexsetup',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            item: 'init',
            window: $(window)[0].innerWidth
        }),
        success: function (res) {
            $(".setup-role").show();
            document.getElementById('setup-org').innerHTML = res;          
        },
        error: function () {
            navError('indexsetup');
        }
    })
})

// Primary Registration
function orgPrimary(org){
    $.ajax({
        url: 'indexsetup',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            item: 'primary',
            window: $(window)[0].innerWidth
        }),
        success: function (res) {
            document.getElementById('setup-org').innerHTML = res;        
        },
        error: function () {
            navError('indexsetup');
        }
    })
}

// Admin Registration
function orgAdmin(org){
    $.ajax({
        url: 'indexsetup',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            item: 'admin',
            window: $(window)[0].innerWidth
        }),
        success: function (res) {
            document.getElementById('setup-org').innerHTML = res;       
        },
        error: function () {
            navError('indexsetup');
        }
    })
}

// License Registration
function orgLicense(org){
    $.ajax({
        url: 'indexsetup',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            item: 'license',
            window: $(window)[0].innerWidth
        }),
        success: function (res) {
            document.getElementById('setup-org').innerHTML = res;        
        },
        error: function () {
            navError('indexsetup');
        }
    })
}
