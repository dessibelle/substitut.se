/*jslint browser: true*/
/*global $, jQuery, substitut*/

(function ($) {
    "use strict";

    var security = {};

    $.extend(true, substitut.modules, {Security: function (options) {

        security = {

            options: $.extend({
                csrftoken: null
            }, options),

            storage: null,

            init: function () {
                try {
                    security.storage = substitut.modules.Storage({name: "security"});
                    if (!security.options.csrftoken) {
                        security.options.csrftoken = security.storage.getCookie('csrftoken');
                    }
                } catch (ex) {
                    if (ex instanceof substitut.exceptions.StorageDisabledException) {
                        console.log("storage is disabled");
                    } else {
                        console.log(ex);
                    }
                }
            },

            /**
             * Return HTTP methods that does not require CSRF protection.
             */
            csrfSafeMethod: function (method) {
                var safe = (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                return safe;
            },

            /**
             * Test that a given url is a same-origin URL.
             * url could be relative or scheme relative or absolute.
             */
            sameOrigin: function (url) {
                var host = document.location.host; // host + port
                var protocol = document.location.protocol;
                var sr_origin = '//' + host;
                var origin = protocol + sr_origin;

                var same = (url === origin || url.slice(0, origin.length + 1) === origin + '/') ||
                        (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') ||
                        // or any other URL that isn't scheme relative or absolute i.e relative.
                        !(/^(\/\/|http:|https:).*/.test(url));
                return same;
            },

            /**
             * Send the token to same-origin, relative URLs only.
             * Send the token only if the method warrants CSRF protection.
             */
            setCsrfHeader: function (xhr, settings) {
                if (!security.csrfSafeMethod(settings.type) && security.sameOrigin(settings.url)) {
                    xhr.setRequestHeader("X-CSRFToken", security.getCsrfToken());
                }
            },

            getCsrfToken: function () {
                return security.options.csrftoken;
            }
        };


        security.init();

        return {
            setCsrfHeader: security.setCsrfHeader,
            getCsrfToken: security.getCsrfToken
        };
    }});
}(jQuery));