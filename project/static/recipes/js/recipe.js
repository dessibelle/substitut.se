/*jslint browser: true*/
/*global $, jQuery, Handlebars, substitut*/

(function ($) {
    "use strict";

    var rec = {};

    $.extend(true, substitut.modules, {Recipe: function (data) {
        rec = {

            data: $.extend({
                id: 0,
                name: '',
                description: '',
                servings: 0,
                instructions: '',
                image: '',
                pub_date: '',
                status: '',
                ingredients: [],
                vote_total: 0,
                url: '',
                weight: 0
            }, data),

            nutrition: {
                //energy_kj: 0,
                energy_kcal: 0,
                protein: 0,
                fat: 0,
                carbohydrates: 0,
                fibers: 0
                //salt: 0,
                //water: 0,
                //saturates: 0,
                //monounsaturated: 0,
                //trans_fat: 0,
                //cholesterol: 0,
                //vitamin_d: 0,
                //vitamin_e: 0,
                //vitamin_k: 0,
                //vitamin_c: 0,
                //vitamin_b6: 0,
                //vitamin_b12: 0,
                //iron: 0
            },

            labels: {
                name: 'Namn',
                unit: 'Enhet',
                amount: 'Mängd',
                energy_kj: 'Energi (kj)',
                energy_kcal: 'Energi (kcal)',
                protein: 'Protein (g)',
                fat: 'Fett (g)',
                carbohydrates: 'Kolhydrater (g)',
                fibers: 'Fibrer (g)',
                salt: 'Salt (g)',
                water: 'Vatten (g)',
                saturates: 'Mättat fett (g)',
                monounsaturated: 'Enkelomättat fett (g)',
                trans_fat: 'Transfetter (g)',
                cholesterol: 'Kolesterol (g)',
                vitamin_d: 'D-vitamin (µg)',
                vitamin_e: 'E-vitamin  (µg)',
                vitamin_k: 'K-vitamin  (µg)',
                vitamin_c: 'C-vitamin  (µg)',
                vitamin_b6: 'Vitamin B6  (µg)',
                vitamin_b12: 'Vitamin B12  (µg)',
                iron: 'Järn (g)'
            },

            init: function () {
                rec.updateNutrition();
            },

            updateNutrition: function () {
                rec.data.ingredients.forEach(function (ingredient) {
                    $.each(ingredient, function (key, value) {
                        if (rec.nutrition.hasOwnProperty(key) && value) {
                            rec.nutrition[key] += parseFloat(value);
                        }
                    });
                });
            },

            getNutrition: function () {
                var kv = [], name, total, per_hundred_gram, per_serving, sum = 0;
                $.each(rec.nutrition, function (key, value) {

                    name = rec.labels[key];
                    total = value;
                    per_hundred_gram = (value / rec.data.weight) * 100;
                    sum += value;

                    if (rec.data.servings) {
                        per_serving = (total / rec.data.servings);
                    } else {
                        per_serving = 0;
                    }

                    if (total !== 0) {
                        kv.push({
                            key: name,
                            val: Math.round(total * 100) / 100,
                            phg: Math.round(per_hundred_gram * 100) / 100,
                            ps: Math.round(per_serving * 100) / 100
                        });
                    }
                });
                return kv;
            },

            getData: function () {
                rec.data.nutrition = rec.getNutrition();
                return rec.data;
            },

            getUrl: function () {
                return rec.data.url;
            }
        };

        rec.init();

        return {
            getData: rec.getData
        };
    }});
}(jQuery));