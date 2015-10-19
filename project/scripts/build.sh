#!/bin/bash

SCRIPTPATH=$(cd $(dirname $0); pwd -P)
ROOTPATH=${SCRIPTPATH}/..
SASSPATH=${ROOTPATH}/sass
STATICPATH=${ROOTPATH}/static
JSPATH=${STATICPATH}/recipes/js

# Final css and js files
CSSFILE=${STATICPATH}/recipes/css/substitut.css
JSFILE=${STATICPATH}/recipes/js/final/app.js

# JS files to be compressed
COMPRESS=(
    ${JSPATH}/vote.js
    ${JSPATH}/exceptions.js
    ${JSPATH}/storage.js
    ${JSPATH}/recipe.js
    ${JSPATH}/substitut.js
    ${JSPATH}/templates/templates.js
)

# Files to be combined into the final js
COMBINE=(
    ${STATICPATH}/lib/jquery/dist/jquery.min.js
    ${STATICPATH}/lib/jquery-ui/jquery-ui.min.js
    ${STATICPATH}/lib/jquery-unveil/jquery.unveil.min.js
    ${STATICPATH}/lib/handlebars/handlebars.runtime.js
    ${STATICPATH}/lib/parallax/parallax.min.js
    ${STATICPATH}/recipes/js/final/substitut.min.js
)

COMPRESS_FILES=$(IFS=" "; echo "${COMPRESS[*]}")
COMBINE_FILES=$(IFS=" "; echo "${COMBINE[*]}")

echo "Compiling css ..."
scss ${SASSPATH}/app.scss > ${CSSFILE}
echo "Done!"

echo "Compiling handlebars templates ..."
handlebars ${STATICPATH}/recipes/js/templates/ > ${STATICPATH}/recipes/js/templates/templates.js
echo "Done!"

echo "Compressing and combining JS ..."
${SCRIPTPATH}/compressjs.sh ${COMPRESS_FILES} ${STATICPATH}/recipes/js/final/substitut.min.js
echo ${COMBINE_FILES} | xargs cat > ${JSFILE}
echo "Done!"
