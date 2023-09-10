if (document.documentElement.clientWidth < 600) {
    document.getElementById("pagination").classList.remove("pagination-lg");
    if (document.documentElement.clientWidth < 480) {
        document.getElementById("pagination").classList.add("pagination-sm");
    }
}

window.onresize = function () {
    if (document.documentElement.clientWidth < 600) {
        document.getElementById("pagination").classList.remove("pagination-lg");
        if (document.documentElement.clientWidth < 480) {
            document.getElementById("pagination").classList.add("pagination-sm");
        }
    } else {
        document.getElementById("pagination").classList.add("pagination-lg");
    }
};