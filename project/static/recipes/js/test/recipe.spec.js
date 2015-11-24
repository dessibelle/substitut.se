/*global substitut, describe, beforeEach, spyOn, it, expect*/
describe("Recipe", function () {
    "use strict";
    var recipe;
    var default_values = {
        name: 'Recipe one',
        description: 'This is the description for recipe one',
        servings: 4,
        weight: 330.5,
        ingredients: [
            {
                multiplier: 1.0,
                vitamin_d: 0.0,
                name: "Sojadryck berikad",
                unit: "Deciliter",
                vitamin_b6: 0.045,
                protein: 4.65,
                vitamin_b12: 0.0,
                fat: 3.5999999999999996,
                trans_fat: 0.0,
                energy_kcal: 66.0,
                text: "Sojamj\u00f6lk",
                cholesterol: 0.0,
                vitamin_k: 0.0,
                unit_short: "dl",
                saturates: 0.0,
                iron: 0.0,
                salt: 0.21000000000000002,
                carbohydrates: 3.75,
                monounsaturated: 0.0,
                energy_kj: 276.0,
                fibers: 0.0,
                vitamin_c: 1.5,
                water: 135.14999999999998,
                amount: 1.5,
                vitamin_e: 0.0
            }
        ]
    };

    beforeEach(function () {
        recipe = new substitut.modules.Recipe(default_values);
    });

    it("should be able to return a label", function () {
        var label = recipe.getLabel('fibers');
        expect(label.val).toEqual('Fibrer');
        expect(label.unit).toEqual('g');
    });

    it("should be able to return recipe data", function () {
        var data = recipe.getData(),
            expected = {
                id: 0,
                name: default_values.name,
                description: default_values.description,
                servings: default_values.servings,
                instructions: '',
                image: '',
                pub_date: '',
                status: '',
                ingredients: default_values.ingredients,
                vote_total: 0,
                url: '',
                weight: default_values.weight,
                nutrition: [
                    {
                        key: 'energy_kcal',
                        name: 'Kalorier',
                        unit: 'kcal',
                        val: 66,
                        phg: 19.97,
                        ps: 16.5
                    },
                    {
                        key: 'protein',
                        name: 'Protein',
                        unit: 'g',
                        val: 4.65,
                        phg: 1.41,
                        ps: 1.16
                    },
                    {
                        key: 'fat',
                        name: 'Fett',
                        unit: 'g',
                        val: 3.6,
                        phg: 1.09,
                        ps: 0.9
                    },
                    {
                        key: 'carbohydrates',
                        name: 'Carbs',
                        unit: 'g',
                        val: 3.75,
                        phg: 1.13,
                        ps: 0.94
                    }
                ]
            };
        expect(data).toEqual(expected);
    });
});