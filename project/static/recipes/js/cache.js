/*jslint browser: true*/
/*global $, jQuery, window, substitut, Handlebars*/
(function ($) {
    "use strict";

    var cache = {};

    $.extend(true, substitut.modules, {Cache: function (options) {

        cache = {

            options: $.extend({
                ttl: 0
            }, options),

            cache: {},
            keys: [],


            index: function (arr, obj) {
                var i = 0;
                arr.forEach(function (item) {
                    if (item === obj) {
                        return i;
                    }
                    i += 1;
                });
                return -1;
            },

            serialize: function (opts) {
                if (opts !== null && typeof opts === 'object') {
                    return $.param(opts);
                } else {
                    return (opts).toString();
                }
            },

            remove: function (key) {
                var t = cache.index(cache.keys, key);
                if (t > -1) {
                    cache.keys.splice(t, 1);
                    delete cache.cache[key];
                }
            },

            removeAll: function () {
                cache.cache = {};
                cache.keys = [];
            },

            add: function (key, obj) {
                if (cache.keys.indexOf(key) === -1) {
                    cache.keys.push(key);
                }
                cache.cache[key] = obj;
                return cache.get(key);
            },

            exists: function (key) {
                return cache.cache.hasOwnProperty(key);
            },

            purge: function (k) {
                var key = k || false;
                if (key) {
                    cache.remove(key);
                } else {
                    cache.removeAll();
                }
                return $.extend(true, {}, cache.cache);
            },

            searchKeys: function (str) {
                var keys = [];
                var rStr;
                rStr = new RegExp('\\b' + str + '\\b', 'i');
                $.each(cache.keys, function (ignore, e) {
                    if (e.match(rStr)) {
                        keys.push(e);
                    }
                });
                return keys;
            },

            get: function (key) {
                var val;
                if (cache.cache[key] !== undefined) {
                    if (cache.cache[key] !== null && typeof cache.cache[key] === 'object') {
                        val = $.extend(true, {}, cache.cache[key]);
                    } else {
                        val = cache.cache[key];
                    }
                }
                return val;
            },

            getKey: function (opts) {
                return cache.serialize(opts);
            },

            getKeys: function () {
                return cache.keys;
            }
        };

        return {
            add: cache.add,
            exists: cache.exists,
            purge: cache.purge,
            searchKeys: cache.searchKeys,
            get: cache.get,
            getKey: cache.getKey,
            getKeys: cache.getKeys
        };
    }});
}(jQuery));