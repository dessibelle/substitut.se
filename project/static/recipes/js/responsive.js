/*jslint browser: true*/
/*global $, jQuery, window, substitut, Handlebars*/

function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, 
            args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

(function ($) {
    "use strict";

    var res = {};

    $.extend(true, substitut.modules, {Responsive: function (data) {
        res = {

            data: $.extend({
                state: null,
                callback: null
            }, data),

            init: function () {
                res.setupDeviceState();
            },

            loadDeviceState: function () {
                var elem = document.getElementById("state-indicator"),
                    state = "md";

                if (elem) {
                    state = window.getComputedStyle(elem,':before').getPropertyValue('content');
                    state = state.replace(/['"]+/g, '');
                }

                return state;
            },

            getState: function () {
                return res.data.state;
            },

            setupDeviceState: function () {
                if (res.data.state === null) {
                    res.data.state = res.loadDeviceState();
                }
                window.addEventListener('resize', debounce(function() {
                    var state = res.loadDeviceState();
                    if (state !== res.data.state) {
                        res.data.state = state;
                        if (typeof res.data.callback === 'function') {
                            res.data.callback.call(this, state);
                        }
                    }
                }, 20));
            }
        };

        res.init();

        return {
            getState: res.getState
        };
    }});
}(jQuery));