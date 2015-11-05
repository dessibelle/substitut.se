/*jslint browser: true*/
/*global $, jQuery, substitut*/
(function ($) {
    "use strict";

    $.extend(true, substitut, {exceptions: {}});

    $.extend(true, substitut.exceptions, {
        RecipeException: function (message) {
            this.name = 'RecipeException';
            this.message = message;
        },
        StorageException: function (message) {
            this.name = 'StorageException';
            this.message = message;
        },
        StorageDisabledException: function (message) {
            this.name = 'StorageDisabledException';
            this.message = message;
        },
        StorageParamNotFoundException: function (message) {
            this.name = 'StorageParamNotFoundException';
            this.message = message;
        },
        StorageParamExpiredException: function (message) {
            this.name = 'StorageParamExpiredException';
            this.message = message;
        }
    });
    substitut.exceptions.RecipeException.prototype = new Error();
    substitut.exceptions.StorageException.prototype = new Error();
    substitut.exceptions.StorageDisabledException.prototype = new Error();
    substitut.exceptions.StorageParamNotFoundException.prototype = new Error();
    substitut.exceptions.StorageParamExpiredException.prototype = new Error();
}(jQuery));