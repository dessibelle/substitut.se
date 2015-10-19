/*jslint browser: true*/
/*global $, jQuery*/
(function ($) {
    "use strict";

    $.recipeException = function (message) {
        this.name = 'recipeException';
        this.message = message;
    };
    $.recipeException.prototype = new Error();

    $.storageException = function (message) {
        this.name = 'storageException';
        this.message = message;
    };
    $.storageException.prototype = new Error();

    $.storageDisabledException = function (message) {
        this.name = 'storageDisabledException';
        this.message = message;
    };
    $.storageDisabledException.prototype = new Error();

    $.storageParamNotFoundException = function (message) {
        this.name = 'storageParamNotFoundException';
        this.message = message;
    };
    $.storageParamNotFoundException.prototype = new Error();

    $.storageParamExpiredException = function (message) {
        this.name = 'storageParamExpiredException';
        this.message = message;
    };
    $.storageParamExpiredException.prototype = new Error();


}(jQuery));