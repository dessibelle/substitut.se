/*jslint browser: true*/
/*global $, jQuery*/
(function ($) {
    "use strict";
    $.storage = function (data) {
        var storage = {

            enabled: true,
            object: null,

            data: $.extend({
                'name': 'undefined',
                'expire': 0
            }, data),

            _init: function () {
                storage.enabled = Storage !== "undefined";
                if (storage.enabled) {
                    if (!localStorage[storage.data.name]) {
                        localStorage.setItem(storage.data.name, "{}");
                    }
                    storage.object = JSON.parse(localStorage.getItem(storage.data.name));
                } else {
                    throw new $.storageDisabledException("localstorage is not supported");
                }
            },

            get: function (param) {
                if (!storage.enabled) {
                    throw new $.storageDisabledException("localstorage is not supported");
                }
                if (storage.object[param] === undefined) {
                    throw new $.storageParamNotFoundException(
                        "param \"" + param + "\" does not exist"
                    );
                }
                var obj = storage.object[param];
                if (storage.data.expire) {
                    var now = new Date().getTime() / 1000;
                    if (now >= obj.timestamp) {
                        delete storage.object[param];
                        localStorage.setItem(storage.data.name, JSON.stringify(storage.object));
                        throw new $.storageParamExpiredException("param \"" + param + "\" found but has expired");
                    }
                    if (obj.value === undefined) {
                        return "";
                    }
                    return obj.value;
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
                if (storage.enabled) {
                    var timestamp = 0;
                    if (storage.data.expire) {
                        timestamp = storage.getTimestamp(storage.data.expire);
                    }
                    if (value === undefined) {
                        storage.object[param] = { 'timestamp': timestamp };
                    } else {
                        storage.object[param] = { 'value': value, 'timestamp': timestamp };
                    }
                    localStorage.setItem(storage.data.name, JSON.stringify(storage.object));
                } else {
                    throw new $.storageDisabledException("localstorage is not supported");
                }
            }
        };
        storage._init();

        return {
            get: storage.get,
            set: storage.set
        };
    };
}(jQuery));