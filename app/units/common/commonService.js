import $ from 'jquery';

var commonService = {
    startLoader: function(targetButton, waitText){
        if (!targetButton){
            return;
        }
        var buttonObject = $(targetButton);
        var icon = buttonObject.find('i');
        if (icon){
            buttonObject[0].oldIcon = icon;
            icon.detach();
        }
        buttonObject[0].oldText = buttonObject.text();
        buttonObject.text(waitText);
        
        buttonObject.prepend('<i class="fas fa-cog fa-spin loader-in-button"></i>');
        buttonObject.prop('disabled', true);
    },
    stopLoader: function(targetButton){
        if (!targetButton){
            return;
        }
        var buttonObject = $(targetButton);
        buttonObject.text(buttonObject[0].oldText);
        if (buttonObject[0].oldIcon){
            buttonObject.prepend(buttonObject[0].oldIcon);
        }
        delete buttonObject[0].oldText;
        delete buttonObject[0].oldIcon;
        buttonObject.find('.icon-span').remove();
        buttonObject.prop('disabled', false);
    }
};
export { commonService };