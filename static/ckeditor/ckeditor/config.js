// static/js/ckeditor_config.js

CKEDITOR.editorConfig = function (config) {
    // Define changes to default configuration here. For example:
    // config.language = 'fr';
    // config.uiColor = '#AADC6E';
    config.allowedContent = true;
    config.extraAllowedContent = 'img[width,height];*(*);*{*}';

    // Add the following lines to set the default width for images to 100%
    config.on = {
        dialogShow: function (e) {
            if (e.data.name === 'image2') {
                e.data.definition.getContents('info').get('txtWidth')['default'] = '100%';
                // You can also set the default height if needed
                // e.data.definition.getContents('info').get('txtHeight')['default'] = '';
            }
        },
    };
};
