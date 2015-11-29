/*jslint browser: true*/
/*global $, jQuery, substitut*/

(function ($) {
    "use strict";

    var storage = {};

    /**
     * Local storage class.
     *
     *
     */
    $.extend(true, substitut.modules, {Storage: function (data) {
        storage = {

            enabled: true,
            object: null,

            data: $.extend({
                name: 'undefined',
                expire: 0
            }, data),

            init: function () {
                storage.enabled = localStorage !== "undefined";
                if (storage.enabled) {
                    if (!localStorage[storage.data.name]) {
                        localStorage.setItem(storage.data.name, "{}");
                    }
                    storage.object = JSON.parse(localStorage.getItem(storage.data.name));
                } else {
                    // @TODO: use getCookie
                    var cookieData = null,
                        objectString = "{}";

                    cookieData = document.cookie.match('(^|;)\\s*' + storage.data.name + '\\s*=\\s*([^;]+)');
                    if (cookieData) {
                        objectString = cookieData.pop();
                    }

                    if (objectString) {
                        storage.object = JSON.parse(objectString);
                    } else {
                        storage.object = {};
                    }
                    document.cookie = storage.data.name + "=" + JSON.stringify(storage.object) + "; path=/";
                }
            },

            get: function (param) {
                if (storage.object[param] === undefined) {
                    throw new substitut.exceptions.StorageParamNotFoundException(
                        "param \"" + param + "\" does not exist"
                    );
                }
                var obj = storage.object[param];
                if (storage.data.expire) {
                    var now = new Date().getTime() / 1000;
                    if (now >= obj.ts) {
                        delete storage.object[param];
                        localStorage.setItem(storage.data.name, JSON.stringify(storage.object));
                        throw new substitut.exceptions.StorageParamExpiredException("param \"" + param + "\" found but has expired");
                    }
                }
                if (obj.val === undefined) {
                    return "";
                }
                return obj.val;
            },

            getTimestamp: function (daysInFuture) {
                if (daysInFuture === undefined) {
                    daysInFuture = 0;
                }
                var now, startOfToday, startOfTomorrow;

                now = new Date();
                startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate()) / 1000;
                startOfTomorrow = (startOfToday + (daysInFuture * 24 * 60 * 60));

                return startOfTomorrow;
            },

            set: function (param, val) {
                var ts = 0;
                if (storage.data.expire) {
                    ts = storage.getTimestamp(storage.data.expire);
                }
                if (val === undefined) {
                    storage.object[param] = {ts: ts};
                } else {
                    storage.object[param] = {val: val, ts: ts};
                }
                if (storage.enabled) {
                    localStorage.setItem(storage.data.name, JSON.stringify(storage.object));
                } else {
                    document.cookie = storage.data.name + "=" + JSON.stringify(storage.object) + "; path=/";
                }
            },

            getCookie: function(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
        };
        storage.init();

        return {
            get: storage.get,
            set: storage.set,
            getCookie: storage.getCookie
        };
    }});
}(jQuery));