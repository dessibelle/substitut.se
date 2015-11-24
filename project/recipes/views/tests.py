from djangojs.views import JasmineView


class SubstitutJasmineView(JasmineView):
    js_files = (
        'js/libs/jquery-1.10.1.js',
        'js/init.js',
        'js/exceptions.js',
        'js/recipe.js',
        'js/responsive.js',
        'js/storage.js',
        'js/vote.js',
        'js/substitut.js',
        'js/test/*.spec.js'
    )
