/*jslint browser: true*/
/*global $, jQuery, window, substitut, Handlebars*/

(function ($) {
    "use strict";

    var app = {};

    $.extend(true, substitut.modules, {Main: function (options) {
        app = {

            cache: {},
            options: $.extend({}, options),
            votes: null,
            limit: 10,
            offset: 0,
            state: null,

            init: function () {
                $.hisrc.speedTest();

                app.setupAutocomplete();
                app.setupSearchPromoteBtn();
                app.setupPagination();
                app.setupNutritionToggle();
                app.loadRecipes();

                // Setup voting functionality
                app.votes = substitut.modules.Vote(
                    {
                        selector: "vote"
                    }
                );
                app.setupVoteButtons();

                // Setup callback on window state change (xxs, xs, sm, md or lg)
                app.state = substitut.modules.Responsive(
                    {
                        callback: app.responsiveChange
                    }
                );

                $(".recipe-image").hisrc({useTransparentGif: true});
            },


            responsiveChange: function (state) {
                if (state === "xxs") {
                    app.votes.expandVoteButton();
                    $("body").removeClass().addClass("substitut-" + state);
                } else if (state === "xs") {
                    app.votes.expandVoteButton();
                    $("body").removeClass().addClass("substitut-" + state);
                } else if (state === "sm") {
                    app.votes.expandVoteButton();
                    $("body").removeClass().addClass("substitut-" + state);
                } else if (state === "md") {
                    app.votes.collapseVoteButton();
                    $("body").removeClass().addClass("substitut-" + state);
                } else if (state === "lg") {
                    app.votes.collapseVoteButton();
                    $("body").removeClass().addClass("substitut-" + state);
                }
            },

            setupSearchPromoteBtn: function () {
                $(".search-promote-btn").on("click", function (ignore) {
                    $("#index-search-field").focus();
                });
            },

            hideFooter: function () {
                $('.site-footer').addClass("hidden");
            },

            showFooter: function () {
                $('.site-footer').removeClass("hidden");
            },

            setupPagination: function () {
                app.limit = parseInt($("#content").attr("data-limit"));
                $(".content-wrapper").on("click", "#show-more-btn", function (event) {
                    $(event.currentTarget).fadeOut("fast", function () {
                        $(".last").removeClass("last");
                        app.loadRecipesAppend();
                    });
                });
            },

            setupVoteButtons: function () {
                $("#content").on("click", app.votes.getSelector(), function (event) {
                    var recipe_id = $(event.currentTarget).attr("data-recipe-id");

                    if (recipe_id !== undefined && !$(event.currentTarget).parent().hasClass("disabled")) {
                        app.votes.voteFor(recipe_id);
                    }

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
                    var my = event.target,
                        recipe_id = $(my).attr("data-recipe-id");

                    if (recipe_id !== undefined) {
                        app.toggleNutrition(my, recipe_id);
                    }

                    event.stopPropagation();
                    return false;
                });
            },

            toggleNutrition: function (e, recipe_id) {
                var $elem, servings, opt, current_index, next, label;

                $elem = $(e);
                servings = $('#servings-recipe-' + recipe_id).html();
                opt = {
                    total: {next: 'phg', label: 'Totalt'},
                    phg: {next: 'total', label: '100g'},
                    ps: {next: 'total', label: 'Portion'}
                };
                if (servings !== undefined) {
                    opt.phg.next = 'ps';
                }

                current_index = $elem.attr('data-current-nutrition');
                next = opt[current_index].next;
                label = opt[next].label;

                $elem.attr('data-current-nutrition', next);
                $elem.html(label);
                $.each(opt, function (key, ignore) {
                    if (key === next) {
                        $('.nutrition-recipe-' + recipe_id + '.nutrition-' + key).show();
                    } else {
                        $('.nutrition-recipe-' + recipe_id + '.nutrition-' + key).hide();
                    }
                });
            },

            parseJson: function (str) {
                if (typeof str === 'object') {
                    return str;
                } else {
                    var json;
                    try {
                        json = JSON.parse(str);
                    } catch (err) {
                        console.log(err);
                        json = null;
                    }
                    return json;
                }
            },

            setupAutocomplete: function () {
                var $searchBox = $('#index-search-field'),
                    $form = $('#index-search-form');
                if ($searchBox) {
                    $searchBox.autocomplete({
                        appendTo: $('.js-header'),
                        minLength: 2,
                        autoFocus: true,
                        source: app.autocompleteSource,
                        select: app.autocompleteSelect
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

            getHtml: function (recipe, last) {
                try {
                    var recipe_id = recipe.id;

                    if (app.cache[recipe_id] === undefined || !app.cache[recipe_id]) {
                        var r = new substitut.modules.Recipe(recipe);
                        app.cache[recipe_id] = r.getData();
                    }
                    if (last) {
                        app.cache[recipe_id].class = "last";
                    }
                    return Handlebars.templates.recipe(app.cache[recipe_id]);
                } catch (err) {
                    console.log(err);
                    return "";
                }
            },

            loadRecipesCallback: function (callback) {
                var endpoint = $('#content').attr('data-endpoint');
                if (endpoint !== undefined && endpoint !== "") {
                    app.loading(true);
                    $.ajax(
                        {
                            url: endpoint,
                            data: {v: Date.now(), o: app.offset}
                        }
                    ).success(callback);
                }
            },

            loadRecipes: function () {
                app.loadRecipesCallback(app.requestSuccess);
            },

            loadRecipesAppend: function () {
                app.loadRecipesCallback(app.requestSuccessAppend);
            },

            hideParallax: function () {
                $(".parallax-window").removeClass("search").addClass("search");
            },

            requestSuccessObject: function (obj) {
                var html, i = 0;

                app.offset += obj.count;
                document.title = obj.label + ' - Substitut';

                obj.data.forEach(function (item) {
                    i += 1;
                    html = app.getHtml(item, (obj.count !== 1 && i === obj.count));
                    app.setContent(html, true);
                    app.votes.getTotal(item.id);
                });

                app.showFooter();

                var state = app.state.getState();
                app.responsiveChange(state);

                $(".recipe-image").hisrc({useTransparentGif: true});
            },

            requestSuccess: function (responseData) {
                var obj = app.parseJson(responseData);
                app.hideParallax();
                if (obj && obj.count > 0) {
                    app.setContent("");
                    app.hideFooter();
                    app.requestSuccessObject(obj);
                }
                app.loading(false);
                if (obj) {
                    app.toggleMoreBtn(obj.count === app.limit);
                }
            },

            requestSuccessAppend: function (responseData) {
                var obj = app.parseJson(responseData);
                app.hideParallax();
                if (obj && obj.count > 0) {
                    $('#show-more-btn').fadeOut("fast", function () {
                        app.requestSuccessObject(obj);
                        app.toggleMoreBtn(obj.count === app.limit);
                    });
                }
                app.loading(false);
            },

            toggleMoreBtn: function (display) {
                if (display) {
                    $('#show-more-btn').removeClass('hidden').show();
                } else {
                    $('#show-more-btn').hide();
                }
            },

            autocompleteSource: function (request, response) {
                $.ajax({
                    url: "/api/terms",
                    data: {term: request.term, v: Date.now()},
                    success: function (responseData) {
                        var array = [], json;

                        json = app.parseJson(responseData);
                        if (json) {
                            json.forEach(function (item) {
                                array.push(
                                    {
                                        value: item.name,
                                        type: item.type,
                                        endpoint: item.endpoint
                                    }
                                );
                            });
                        }
                        response(array);
                    }
                });
            },

            autocompleteSelect: function (ignore, ui) {
                if (ui.item.endpoint !== undefined && ui.item.endpoint !== "") {
                    app.loading(true);
                    app.offset = 0; // Reset offset
                    app.setEndpoint(ui.item.endpoint);

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
                window.history.pushState({content: $content.html()}, "", url);
            },

            setEndpoint: function (endpoint) {
                $("#content").attr("data-endpoint", endpoint);
            },

            clearSearch: function () {
                $('#index-search-field').val("");
            },

            setContent: function (content, append) {
                var $content;

                if (content === undefined || content === "") {
                    $('#content').html("");
                } else {
                    $content = $(content);
                    $content.hide();
                    if (append === 'undefined' || append === false) {
                        $('#content').html("");
                    }
                    $content.appendTo("#content");
                    $content.fadeIn("slow");
                }
            }
        };

        app.init();

        return {
            init: app.init,
            parseJson: app.parseJson,
            responsiveChange: app.responsiveChange
        };
    }});
}(jQuery));
