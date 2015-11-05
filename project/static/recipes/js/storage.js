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
                    if (now >= obj.timestamp) {
                        delete storage.object[param];
                        localStorage.setItem(storage.data.name, JSON.stringify(storage.object));
                        throw new substitut.exceptions.StorageParamExpiredException("param \"" + param + "\" found but has expired");
                    }
                }
                if (obj.value === undefined) {
                    return "";
                }
                return obj.value;
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

            set: function (param, value) {
                var timestamp = 0;
                if (storage.data.expire) {
                    timestamp = storage.getTimestamp(storage.data.expire);
                }
                if (value === undefined) {
                    storage.object[param] = {timestamp: timestamp};
                } else {
                    storage.object[param] = {value: value, timestamp: timestamp};
                }
                if (storage.enabled) {
                    localStorage.setItem(storage.data.name, JSON.stringify(storage.object));
                } else {
                    document.cookie = storage.data.name + "=" + JSON.stringify(storage.object) + "; path=/";
                }
            }
        };
        storage.init();

        return {
            get: storage.get,
            set: storage.set
        };
    }});
}(jQuery));