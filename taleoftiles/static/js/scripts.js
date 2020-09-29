!function() {
    "use strict";
    function t(e, t) {
        e.preventDefault(),
        e.stopPropagation();
        var n, o = document.querySelector(".overlay.visible");
        o && o !== t && o.classList.remove("visible"),
        (n = t).classList.contains("visible") || window.addEventListener("click", function() {
            c(n)
        }),
        t.classList.toggle("visible"),
        "overlayAuth" === t.id && t.classList.contains("visible") && document.getElementById("loginEmail").focus()
    }
    function c(e) {
        e.classList.remove("visible")
    }
    function o(e) {
        r = e,
        [].forEach.call(n, function(e) {
            e.classList.remove("selected")
        }),
        n[r].classList.add("selected"),
        i.style.webkitTransform = "translateX(-" + 100 * r + "%)",
        i.style.transform = "translateX(-" + 100 * r + "%)"
    }
    var n, i, e, l, r, s, a, d, u, v;
    ("ontouchstart"in window || 0 < navigator.MaxTouchPoints || 0 < navigator.msMaxTouchPoints) && document.body.classList.add("touch"),
    window.onscroll = function() {
        var e = document.querySelector("header");
        56 < document.documentElement.scrollTop ? e.classList.add("compact") : e.classList.remove("compact")
    }
    ,
    document.querySelectorAll(".nav-dropdown").forEach(function(e) {
        e.querySelector("div:first-child").addEventListener("click", function() {
            this.parentElement.querySelector(".nav-dropdown-options").classList.add("visible")
        }),
        e.addEventListener("mouseleave", function() {
            this.querySelector(".nav-dropdown-options").classList.remove("visible")
        })
    }),
    document.querySelectorAll(".nav-dropdown-options > div").forEach(function(e) {
        e.addEventListener("click", function() {
            this.parentElement.classList.remove("visible")
        })
    }),
    document.querySelectorAll(".btn-tree").forEach(function(e) {
        e.addEventListener("click", function() {
            var e;
            this.classList.contains("btn-tree-open") || (e = this.parentElement.querySelector(".openable")).style.setProperty("--tree-height", e.scrollHeight + "px"),
            this.classList.toggle("btn-tree-open")
        })
    }),
    i = document.querySelector(".product-gallery-container"),
    e = document.querySelectorAll(".product-gallery-item"),
    l = document.querySelector(".product-gallery-controls ul"),
    r = 0,
    s = e.length,
    a = document.getElementById("gallerybtn-prev"),
    d = document.getElementById("gallerybtn-next"),
    
    [].forEach.call(e, function(e, t) {
        e.dataset.id = t;
        var n = document.createElement("li");
        l.appendChild(n),
        n.addEventListener("click", function() {
            o(t)
        })
    }),
    n = l.querySelectorAll("li"),
    d.addEventListener("click", function() {
        s - 1 <= r || o(+e[++r].dataset.id)
    }),
    a.addEventListener("click", function() {
        r <= 0 || o(+e[--r].dataset.id)
    }),
    o(0),
    document.querySelectorAll("[data-overlay]").forEach(function(e) {
        e.addEventListener("click", function(e) {
            t(e, document.getElementById("overlay" + this.dataset.overlay))
        })
    }),
    document.querySelectorAll(".overlay-title .btn").forEach(function(e) {
        e.addEventListener("click", function() {
            c(this.parentElement.parentElement)
        })
    }),
    document.querySelectorAll(".overlay").forEach(function(e) {
        e.addEventListener("click", function(e) {
            e.stopPropagation()
        })
    }),
    u = document.querySelector(".notification"),
    (v = document.getElementById("btnAddToCart")) && v.addEventListener("click", function() {
        u.classList.add("visible"),
        setTimeout(function() {
            u.classList.remove("visible")
        }, 3e3)
    })
}(window);


