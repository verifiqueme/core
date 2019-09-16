var express = require('express');
var app = express();

const GoogleNewsRss = require('google-news-rss');

const googleNews = new GoogleNewsRss();

app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.set('port', process.env.PORT || 8083);
app.get('/search/:query', function (req, res, next) {
    var query = req.params.query;
    var data = {"articles": []}
    if(req.query.lang){
        googleNews
            .search(query,num = 30, language = req.query.lang)
            .then(resp => {
                data.articles = resp;
                res.send(data);
            }).catch(error => {
            res.send({"error": 'true', "articles": []});
        });
    } else {
        res.status(400).send({'error': 'language is required'});
    }

});

app.get('/hi', function (req, res, next) {
    res.status(200).send({'ping': 'pong'});
});

app.listen(app.get('port'), function () {
    console.log('Node app is running on port', app.get('port'));
});
