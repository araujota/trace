
var XMLHttpRequest = require('xhr2');
const jsdom = require("jsdom");
const { response } = require('express');
// var req = new XMLHttpRequest();  
// req.open('GET', 'https://www.nytimes.com/2024/04/21/us/politics/trump-trial-analysis.html', false);   
// req.send(null);  
// if(req.status == 200)  
//    dump(req.responseText);

   function initialSearch() {
    const dom = new jsdom.JSDOM(`<!DOCTYPE html><p>Hello world</p>`);

    var xhr = new XMLHttpRequest();
    xhr.addEventListener("load", function() {
        responseDOM = new jsdom.JSDOM(xhr.response);
        let domtext = responseDOM.window.document.querySelector("article").textContent
        console.log(domtext)
    }, false);
    xhr.open('GET', "https://www.nbcnews.com/politics/2024-election/rfk-jr-candidacy-hurts-trump-biden-nbc-news-poll-finds-rcna148536");
    xhr.send();
}

initialSearch()
