/*jslint browser: true*/
/*global $, jQuery, substitut*/

(function ($) {
    "use strict";

    var vote = {};

    $.extend(true, substitut.modules, {Vote: function (options) {

        vote = {

            options: $.extend({}, options),
            storage: null,

            init: function () {
                try {
                    vote.storage = substitut.modules.Storage({
                        name: "votes",
                        expire: 1 // expire next day
                    });
                } catch (ex) {
                    if (ex instanceof substitut.exceptions.StorageDisabledException) {
                        console.log("storage is disabled");
                    } else {
                        console.log(ex);
                    }
                }
            },

            save: function (recipe_id) {
                if (vote.storage) {
                    try {
                        vote.storage.get(recipe_id);
                    } catch (ex) {
                        if (ex instanceof substitut.exceptions.StorageParamNotFoundException) {
                            vote.storage.set(recipe_id);
                        }
                    }
                }
            },

            voteFor: function (recipe_id) {
                $.ajax({
                    url: "/api/recipes/vote/" + recipe_id + "/?v=" + Date.now(),
                    success: function (responseData) {
                        var json = substitut.application.parseJson(responseData);
                        if (json) {
                            if (json.status === "ok") {
                                vote.save(recipe_id);
                            } else if (json.status === "denied") {
                                vote.save(recipe_id);
                            } else {
                                console.log("Endpoint returned an unknown status: ", json.status);
                            }
                            vote.validateButton(recipe_id);
                        }
                    }
                });
            },

            /**
             * Checks if vote button should be enabled for current recipe.
             */
            validateButton: function (recipe_id) {
                var $vote_total = $('#recipe-footer-row-' + recipe_id);
                try {
                    vote.storage.get(recipe_id);
                    if (!$vote_total.hasClass("hidden")) {
                        $vote_total.fadeOut("fast", function (event) {
                            $(event.currentTarget).addClass("hidden");
                        });
                    }
                } catch (ex) {
                    if (ex instanceof substitut.exceptions.StorageParamNotFoundException) {
                        $vote_total.removeClass("hidden");
                    }
                }
            },
        };

        vote.init();

        return {
            voteFor: vote.voteFor,
            validateButton: vote.validateButton,
            save: vote.save
        };
    }});
}(jQuery));