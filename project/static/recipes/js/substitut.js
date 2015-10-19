/*jslint browser: true*/
/*global $, jQuery*/
(function ($) {
    "use strict";
    $.substitut = function (options) {
        var app = {

            cache: {},
            options: $.extend({}, options),
            votes: null,

            _init: function () {
                app.votes = $.votes({"selector": ".votes-btn"});
                app.setupAutocomplete();
                app.setupVoteButtons();
                app.setupNutritionToggle();
                app.loadRecipes();
            },

            setupVoteButtons: function () {
                $("#content").on("click", app.votes.getSelector(), function (event) {
                    var recipe_id = $(this).attr("data-recipe-id");
                    if (recipe_id !== undefined && !$(this).parent().hasClass("disabled")) {
                        app.votes.voteFor(recipe_id);
                    }
                    event.stopPropagation();
                    return false;
                });
            },

            loading: function (is_loading) {
                var $icon = $('#index-search-btn .glyphicon');
                if ($icon) {
                    if (is_loading) {
                        $icon.removeClass("glyphicon-search").addClass('glyphicon-refresh spinning');
                    } else {
                        $icon.removeClass('glyphicon-refresh spinning').addClass('glyphicon-search');
                    }
                }
            },

            setupNutritionToggle: function () {
                $("#content").on("click", ".nutrition-toggle", function (event) {
                    var my = this,
                        recipe_id = $(my).attr("data-recipe-id");

                    if (recipe_id !== undefined) {
                        app.toggleNutrition(my, recipe_id);
                    }

                    event.stopPropagation();
                    return false;
                });
            },

            toggleNutrition: function (e, recipe_id) {
                var k = null,
                    $elem = $(e),
                    servings = $('#servings-recipe-' + recipe_id).html(),
                    opt = {
                        'total': {'next': 'phg', 'label': 'totalt'},
                        'phg': {'next': (servings === undefined ? 'total' : 'ps'), 'label': '100g'},
                        'ps': {'next': 'total', 'label': 'portion'}
                    },
                    current_index = $elem.attr('data-current-nutrition'),
                    next = opt[current_index].next,
                    label = opt[next].label;

                $elem.attr('data-current-nutrition', next);
                $elem.html(label);

                for (k in options) {
                    if (options.hasOwnProperty(k)) {
                        if (k === next) {
                            $('.nutrition-recipe-' + recipe_id + '.nutrition-' + k).show();
                        } else {
                            $('.nutrition-recipe-' + recipe_id + '.nutrition-' + k).hide();
                        }
                    }
                }
            },

            parseJson: function (str) {
                var json;
                try {
                    json = JSON.parse(str);
                } catch (err) {
                    console.log(err);
                    json = null;
                }
                return json;
            },

            setupAutocomplete: function () {
                var $searchBox = $('#index-search-field'),
                    $form = $('#index-search-form');
                if ($searchBox) {
                    $searchBox.autocomplete({
                        appendTo: $('.js-header'),
                        source: this.autocompleteSource,
                        select: this.autocompleteSelect
                    });
                }

                if ($form) {
                    $form.submit(function (event) {
                        event.stopPropagation();
                        app.clearSearch();
                        return false;
                    });
                }
            },

            getHtml: function (recipe) {
                try {
                    var recipe_id = recipe.id;
                    if (app.cache[recipe_id] === undefined) {
                        app.cache[recipe_id] = $.recipe(recipe);
                    }
                    return app.cache[recipe_id].getHtml();
                } catch (err) {
                    console.log(err);
                    return "";
                }
            },

            loadRecipes: function () {
                var endpoint = $('#content').attr('data-endpoint');
                if (endpoint !== undefined && endpoint !== "") {
                    app.loading(true);
                    $.ajax({ url: endpoint + "?v=" + Date.now()}).success(app.requestSuccess);
                }
            },

            setSubHeader: function (data) {
                var $subheader = $(".parallax-window");
                $subheader.html("<a href=\"" + data.url + "\">" + data.label + "</a>");
                $(".parallax-window").addClass("search");
            },

            requestSuccess: function (responseData) {
                var i, html, obj;

                obj = app.parseJson(responseData);

                if (obj && obj.count > 0) {
                    app.setContent("");
                    app.setSubHeader(obj);
                    for (i = 0; i < obj.data.length; i++) {
                        html = app.getHtml(obj.data[i]);
                        app.setContent(html, true);
                        app.votes.getTotal(obj.data[i].id);
                    }
                    $(".recipe-image").unveil(200, app.unveil);
                }

                app.loading(false);
            },

            autocompleteSource: function (request, response) {
                $.ajax({
                    url: "/api/terms",
                    data: {'term': request.term, "v": Date.now()},
                    success: function (responseData) {
                        var i, array = [], json;

                        json = app.parseJson(responseData);
                        if (json) {
                            for (i = 0; i < json.length; i++) {
                                array.push(
                                    {
                                        'value': json[i].name,
                                        'type': json[i].type,
                                        'endpoint': json[i].endpoint
                                    }
                                );
                            }
                        }
                        response(array);
                    }
                });
            },
            autocompleteSelect: function (ignore, ui) {
                if (ui.item.endpoint !== undefined && ui.item.endpoint !== "") {
                    app.loading(true);
                    $.ajax({
                        url: ui.item.endpoint
                    }).success(app.requestSuccess).done(function (responseData) {
                        var obj = app.parseJson(responseData);
                        if (obj) {
                            app.setUrl(obj.url);
                        }
                        app.clearSearch();
                    });
                }
            },

            setUrl: function (url) {
                var $content = $("#content");
                window.history.pushState({"content": $content.html()}, "", url);
            },

            clearSearch: function () {
                $('#index-search-field').val("");
            },

            setContent: function (content, append) {
                if (append !== 'undefined' && append === true) {
                    $('#content').append(content);
                } else {
                    $('#content').html(content);
                }
            },

            unveil: function () {
                var $me = $(this);
                $me.removeClass("image-hidden").addClass("image-visible");
            }
        };
        app._init();
        return {
            parseJson: app.parseJson,
            unveil: app.unveil
        };
    };
}(jQuery));


$(function () {
    "use strict";
    $.app = $.substitut();
    window.onpopstate = function (e) {
        if (e.state) {
            $("#content").html(e.state.content);
        }
    };
});