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
                        return true;
                    } catch (ex) {
                        if (ex instanceof substitut.exceptions.StorageParamNotFoundException) {
                            vote.storage.set(recipe_id);
                            return false;
                        }
                    }
                }
                return false;
            },

            voteHide: function (recipe_id) {
                vote.save(recipe_id);
                vote.validateButton(recipe_id);
            },

            voteUp: function (recipe_id) {
                vote.voteFor(recipe_id, 'up');
            },

            voteDown: function (recipe_id) {
                vote.voteFor(recipe_id, 'down');
            },

            voteSuccess: function (responseData) {
                var json = substitut.application.parseJson(responseData);
                if (json) {
                    if (json.status === "ok") {
                        vote.save(json.recipe_id);
                    } else if (json.status === "denied") {
                        vote.save(json.recipe_id);
                    } else {
                        console.log("Endpoint returned an unknown status: ", json.status);
                    }
                    vote.validateButton(json.recipe_id);
                }
            },

            voteFor: function (recipe_id, vote_type) {
                console.log("voteFor");
                $.ajax(
                    {
                        url: "/api/recipes/vote/" + recipe_id + "/?v=" + Date.now(),
                        data: {type: vote_type},
                        method: 'POST',
                        success: vote.voteSuccess,
                        beforeSend: substitut.application.setCsrfHeader
                    }
                );
            },

            /**
             * Checks if vote button should be enabled for current recipe.
             */
            validateButton: function (recipe_id) {
                var $vote_total = $('#recipe-vote-wrapper-' + recipe_id);
                try {
                    vote.storage.get(recipe_id);
                    if (!$vote_total.hasClass("hidden")) {
                        $vote_total.fadeOut("fast", function (event) {
                            if (event && event.currentTarget) {
                                $(event.currentTarget).addClass("hidden");
                            }
                        });
                    }
                } catch (ex) {
                    if (ex instanceof substitut.exceptions.StorageParamNotFoundException) {
                        $vote_total.removeClass("hidden");
                    }
                }
            }
        };

        vote.init();

        return {
            voteUp: vote.voteUp,
            voteDown: vote.voteDown,
            hide: vote.voteHide,
            validateButton: vote.validateButton,
            save: vote.save
        };
    }});
}(jQuery));