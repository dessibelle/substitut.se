/*jslint browser: true*/
/*global $, jQuery*/
(function ($) {
    "use strict";
    $.votes = function (options) {
        var vote = {

            options: $.extend({
                "selector": ".vote-btn"
            }, options),
            storage: null,

            _init: function () {
                try {
                    vote.storage = $.storage({
                        "name": "votes",
                        "expire": 1 // expire next day
                    });
                } catch (ex) {
                    if (ex instanceof $.storageDisabledException) {
                        // TODO: fall back on cookies
                        console.log("storage is disabled");
                    }
                }
            },

            save: function (recipe_id) {
                if (vote.storage) {
                    try {
                        vote.storage.get(recipe_id);
                    } catch (ex) {
                        if (ex instanceof $.storageParamNotFoundException) {
                            vote.storage.set(recipe_id);
                        }
                    }
                }
            },

            voteFor: function (recipe_id) {
                $.ajax({
                    url: "/api/recipes/vote/" + recipe_id + "/?v=" + Date.now(),
                    success: function (responseData) {
                        var json = $.app.parseJson(responseData);
                        if (json) {
                            if (json.status === "ok") {
                                var $vote_total = $('#votes-total-' + recipe_id);
                                if ($vote_total) {
                                    vote.save(recipe_id);
                                    var num_votes = parseInt($vote_total.html(), 10) + 1;
                                    vote.setTotal({'recipe_id': recipe_id, 'votes': num_votes});
                                }
                            } else if (json.status === "denied") {
                                vote.save(recipe_id);
                            }
                            vote.validateButton(recipe_id);
                        }
                    }
                });
            },

            getTotal: function (recipe_id) {
                $.ajax({
                    url: "/api/recipes/votes/" + recipe_id + "/?v=" + Date.now(),
                    success: function (responseData) {
                        var json = $.app.parseJson(responseData);
                        if (json) {
                            vote.setTotal(json);
                        }
                    }
                });
            },

            validateButton: function (recipe_id) {
                var $vote_total = $('#votes-total-' + recipe_id);
                if (!$vote_total.parent().hasClass("disabled")) {
                    $vote_total.parent().addClass("disabled");
                }
                try {
                    vote.storage.get(recipe_id);
                } catch (ex) {
                    if (ex instanceof $.storageParamNotFoundException) {
                        $vote_total.parent().removeClass("disabled");
                    }
                }
            },

            setTotal: function (json) {
                if (json.recipe_id === undefined) {
                    throw new Error("setVoteTotal(): Recipe id is not set");
                }
                if (json.votes === undefined) {
                    throw new Error("setVoteTotal(): Votes is not set");
                }
                var $vote_total = $('#votes-total-' + json.recipe_id);
                if (!$vote_total) {
                    throw new Error("setVoteTotal(): Element #votes-total-" + json.recipe_id + " not found");
                }
                $vote_total.html(json.votes);
                vote.validateButton(json.recipe_id);
            },

            getSelector: function () {
                return vote.options.selector;
            }
        };

        vote._init();

        return {
            voteFor: vote.voteFor,
            getTotal: vote.getTotal,
            getSelector: vote.getSelector
        };
    };
}(jQuery));