const axios = require('axios');

var httpService = {
    init: function(csrftoken){
        axios.defaults.headers.common = {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken
            };
    },
    formFullUrl: function(rootUrl, entityUrl){
        var url = '';
        if (rootUrl && entityUrl){
            var delimiter = (rootUrl[rootUrl.length - 1] == '/' ? '' : '/');
            url = rootUrl + delimiter + entityUrl;
        }
        return url;
    },
    post: function (url, data) {
        return axios.post(url, data); 
    },
    get: function(url){
        return axios.get(url);
    }
};
httpService.init(window.csrf_token);
export { httpService };