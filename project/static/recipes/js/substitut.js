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
            security: null,
            limit: 10,
            offset: 0,
            state: null,

            init: function () {
                $.hisrc.speedTest();

                app.security = substitut.modules.Security();
                app.cache = substitut.modules.Cache();

                app.setupAutocomplete();
                app.setupSearchPromoteBtn();
                app.setupPagination();
                app.loadRecipes();
                app.setupFlowtype();

                // Setup voting functionality
                app.votes = substitut.modules.Vote();
                app.setupVoteButtons();


                // Setup callback on window state change (xxs, xs, sm, md or lg)
                app.state = substitut.modules.Responsive(
                    {
                        callback: app.responsiveChange
                    }
                );

                $(".recipe-image").hisrc({useTransparentGif: true});

            },

            setupFlowtype: function () {
                $('.flowtype').flowtype({
                    minFont: 11,
                    maxFont: 40,
                    minimum: 205,
                    maximum: 400,
                    fontRatio: 20
                });
                $('.index-text').flowtype({
                    minFont: 14,
                    maxFont: 40,
                    minimum: 500,
                    maximum: 1200,
                    fontRatio: 30
                });
            },

            responsiveChange: function (state) {
                if (state === "xxs") {
                    $("body").removeClass().addClass("substitut-" + state);
                } else if (state === "xs") {
                    $("body").removeClass().addClass("substitut-" + state);
                } else if (state === "sm") {
                    $("body").removeClass().addClass("substitut-" + state);
                } else if (state === "md") {
                    $("body").removeClass().addClass("substitut-" + state);
                } else if (state === "lg") {
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
                $("#content").on("click", ".vote-up-button", function (event) {
                    var recipe_id = $(event.currentTarget).parent().parent().attr("data-recipe-id");
                    if (recipe_id !== undefined) {
                        if (!$(event.currentTarget).parent().parent().hasClass("hidden")) {
                            app.votes.voteUp(recipe_id);
                        }
                    }
                    return false;
                });
                $("#content").on("click", ".vote-down-button", function (event) {
                    var recipe_id = $(event.currentTarget).parent().parent.attr("data-recipe-id");
                    if (recipe_id !== undefined) {
                        if (!$(event.currentTarget).parent().parent().hasClass("hidden")) {
                            app.votes.voteDown(recipe_id);
                        }
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

            parseJson: function (str) {
                if (str !== null && typeof str === 'object') {
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
                    var opts = {
                        recipe_id: recipe.id
                    };
                    var cache_key = app.cache.getKey(opts);
                    var result = null;

                    if (app.cache.exists(cache_key)) {
                        result = app.cache.get(cache_key);
                    } else {
                        var r = new substitut.modules.Recipe(recipe);
                        result = r.getData();
                        app.cache.add(cache_key, result);
                    }
                    if (last) {
                        result.class = "last";
                    }
                    return Handlebars.templates.recipe(result);
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
                            beforeSend: app.security.setCsrfHeader,
                            url: endpoint,
                            data: {v: Date.now(), o: app.offset},
                            method: 'POST'
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
                    app.votes.validateButton(item.id);
                });

                app.showFooter();

                var state = app.state.getState();
                app.responsiveChange(state);

                $('.instructions, .ingredients > li').flowtype({
                    minFont: 14,
                    maxFont: 26,
                    minimum: 500,
                    maximum: 1200,
                    fontRatio: 30
                });

                $(".recipe-image").hisrc({useTransparentGif: true});
                $('[data-toggle="popover"]').popover(
                    {
                        html: true,
                        title: app.nutritionPopoverTitle,
                        content: app.nutritionPopoverContent,
                        placement: 'bottom',
                        trigger: 'hover'
                    }
                );
            },

            nutritionPopoverTitle: function () {
                var recipe = new substitut.modules.Recipe();
                return recipe.getLabel($(this).attr('data-key')).val || "";
            },

            nutritionPopoverContent: function () {
                var context = {
                    phg: $(this).attr('data-phg'),
                    ps: $(this).attr('data-ps'),
                    info: $(this).attr('data-info')
                };
                return Handlebars.templates.tooltip(context);
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
                    beforeSend: app.security.setCsrfHeader,
                    method: 'POST',
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
                        url: ui.item.endpoint,
                        method: 'POST',
                        beforeSend: app.security.setCsrfHeader
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
            responsiveChange: app.responsiveChange,
            setCsrfHeader: app.security.setCsrfHeader
        };
    }});
}(jQuery));
