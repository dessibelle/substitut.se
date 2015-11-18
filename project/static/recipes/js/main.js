/*jslint browser: true*/
/*global $, jQuery, window, substitut*/
$(function () {
    "use strict";
    $.extend(true, substitut, {application: substitut.modules.Main()});

    window.onpopstate = function (e) {
        if (e.state) {
            $("#content").html(e.state.content);
        }
    };
});
