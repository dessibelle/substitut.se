(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['recipe'] = template({"1":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : {}, alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "                    <div class=\"servings\">\n                        <span id=\"servings-recipe-"
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "\">"
    + alias4(((helper = (helper = helpers.servings || (depth0 != null ? depth0.servings : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"servings","hash":{},"data":data}) : helper)))
    + "</span> portioner\n                    </div>\n";
},"3":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : {}, alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "                    <a class=\"btn btn-tag\" href=\""
    + alias4(((helper = (helper = helpers.url || (depth0 != null ? depth0.url : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"url","hash":{},"data":data}) : helper)))
    + "\">\n                        "
    + alias4(((helper = (helper = helpers.name || (depth0 != null ? depth0.name : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"name","hash":{},"data":data}) : helper)))
    + "\n                    </a>\n";
},"5":function(container,depth0,helpers,partials,data) {
    var stack1, helper;

  return "                    <div class=\"description\">\n                        "
    + ((stack1 = ((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : {},{"name":"description","hash":{},"data":data}) : helper))) != null ? stack1 : "")
    + "\n                    </div>\n";
},"7":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : {}, alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "                            <li>\n                                <span class=\"ingredient-amount\">"
    + alias4(((helper = (helper = helpers.amount || (depth0 != null ? depth0.amount : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"amount","hash":{},"data":data}) : helper)))
    + "</span>\n                                <span class=\"ingredient-unit\">"
    + alias4(((helper = (helper = helpers.unit_short || (depth0 != null ? depth0.unit_short : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"unit_short","hash":{},"data":data}) : helper)))
    + "</span>\n                                <span class=\"ingredient-name\">"
    + alias4(((helper = (helper = helpers.text || (depth0 != null ? depth0.text : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"text","hash":{},"data":data}) : helper)))
    + "</span>\n                            </li>\n";
},"9":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : {}, alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "        <aside class=\"thumbnail recipe-image-wrapper\">\n            <img class=\"recipe-image img-responsive\" src=\"http://127.0.0.1:8000/static/recipes/images/"
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "_135x135.jpg\" data-1x=\"http://127.0.0.1:8000/static/recipes/images/"
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "_270x270.jpg\" data-2x=\"http://127.0.0.1:8000/static/recipes/images/"
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "_540x540.jpg\" width=\"100%\">\n            <div class=\"caption\">\n                <h3>"
    + alias4(((helper = (helper = helpers.name || (depth0 != null ? depth0.name : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"name","hash":{},"data":data}) : helper)))
    + "</h3>\n            </div>\n        </aside>\n";
},"11":function(container,depth0,helpers,partials,data,blockParams,depths) {
    var stack1;

  return ((stack1 = helpers["if"].call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.val : depth0),{"name":"if","hash":{},"fn":container.program(12, data, 0, blockParams, depths),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"12":function(container,depth0,helpers,partials,data,blockParams,depths) {
    var helper, alias1=depth0 != null ? depth0 : {}, alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, alias5=container.lambda;

  return "                    <tr>\n                        <th>"
    + alias4(((helper = (helper = helpers.key || (depth0 != null ? depth0.key : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"key","hash":{},"data":data}) : helper)))
    + "</th>\n                        <td class=\"nutrition-recipe-"
    + alias4(alias5((depths[1] != null ? depths[1].id : depths[1]), depth0))
    + " nutrition-total\">"
    + alias4(((helper = (helper = helpers.val || (depth0 != null ? depth0.val : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"val","hash":{},"data":data}) : helper)))
    + "</td>\n                        <td class=\"nutrition-recipe-"
    + alias4(alias5((depths[1] != null ? depths[1].id : depths[1]), depth0))
    + " nutrition-phg\">"
    + alias4(((helper = (helper = helpers.phg || (depth0 != null ? depth0.phg : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"phg","hash":{},"data":data}) : helper)))
    + "</td>\n                        <td class=\"nutrition-recipe-"
    + alias4(alias5((depths[1] != null ? depths[1].id : depths[1]), depth0))
    + " nutrition-ps\">"
    + alias4(((helper = (helper = helpers.ps || (depth0 != null ? depth0.ps : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"ps","hash":{},"data":data}) : helper)))
    + "</td>\n                    </tr>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data,blockParams,depths) {
    var stack1, helper, alias1=depth0 != null ? depth0 : {}, alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<div class=\"row recipe-row "
    + alias4(((helper = (helper = helpers["class"] || (depth0 != null ? depth0["class"] : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"class","hash":{},"data":data}) : helper)))
    + "\">\n    <div class=\"cover\"></div>\n    <div class=\"column-1 col-md-9 col-sm-12 col-xs-12\">\n        <section class=\"recipe-section\">\n            <article class=\"recipe\">\n                <div class=\"row\">\n                    <h2><a href=\""
    + alias4(((helper = (helper = helpers.url || (depth0 != null ? depth0.url : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"url","hash":{},"data":data}) : helper)))
    + "\">"
    + alias4(((helper = (helper = helpers.name || (depth0 != null ? depth0.name : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"name","hash":{},"data":data}) : helper)))
    + "</a></h2>\n                    <div class=\"vote\" data-recipe-id=\""
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "\">\n                        <span class=\"votes-btn\"><i class=\"glyphicon glyphicon-heart\"></i></span>\n                        <span class=\"votes-text\">Rekommendera</span>\n                        <span class=\"votes-total\" id=\"votes-total-"
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "\">"
    + alias4(((helper = (helper = helpers.vote_total || (depth0 != null ? depth0.vote_total : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"vote_total","hash":{},"data":data}) : helper)))
    + "</span>\n                    </div>\n                </div>\n                <div class=\"row\">\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.servings : depth0),{"name":"if","hash":{},"fn":container.program(1, data, 0, blockParams, depths),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + ((stack1 = helpers.each.call(alias1,(depth0 != null ? depth0.food_groups : depth0),{"name":"each","hash":{},"fn":container.program(3, data, 0, blockParams, depths),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.description : depth0),{"name":"if","hash":{},"fn":container.program(5, data, 0, blockParams, depths),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "                </div>\n                <div class=\"row\">\n                    <div class=\"col-md-4 col-sm-12 col-xs-12 no-left-padding ingredients-wrapper\">\n                        <ul class=\"ingredients\">\n"
    + ((stack1 = helpers.each.call(alias1,(depth0 != null ? depth0.ingredients : depth0),{"name":"each","hash":{},"fn":container.program(7, data, 0, blockParams, depths),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "                        </ul>\n                    </div>\n                    <div class=\"col-md-8 instructions-wrapper\">\n                        <div class=\"instructions\">\n                            "
    + ((stack1 = ((helper = (helper = helpers.instructions || (depth0 != null ? depth0.instructions : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"instructions","hash":{},"data":data}) : helper))) != null ? stack1 : "")
    + "\n                        </div>\n                    </div>\n                </div>\n            </article>\n        </section>\n    </div>\n    <div class=\"column-2 col-md-3 col-sm-12 col-xs-12\">\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.image : depth0),{"name":"if","hash":{},"fn":container.program(9, data, 0, blockParams, depths),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "        <aside class=\"nutrition\">\n            <h3><span class=\"pull-left\">Näring</span> <a href=\"#\" class=\"nutrition-toggle btn btn-info pull-right\" data-recipe-id=\""
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "\" data-current-nutrition=\"total\">totalt</a></h3>\n            <table class=\"nutrition-table\">\n"
    + ((stack1 = helpers.each.call(alias1,(depth0 != null ? depth0.nutrition : depth0),{"name":"each","hash":{},"fn":container.program(11, data, 0, blockParams, depths),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "            </table>\n            <span class=\"footnote\">Källa: <a href=\"http://www.livsmedelsverket.se/livsmedelsdatabasen\" target=\"_blank\">Livsmedelsverket</a></span>\n        </aside>\n    </div>\n</div>\n";
},"useData":true,"useDepths":true});
})();
