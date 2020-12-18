var express = require('express');
var router = express.Router();

//find webtoon info by title_id
function find_webtoon(title_id, callback){
    var sqlquery = "SELECT * FROM webtoons WHERE title_id=?";
    connection.query(sqlquery, title_id,function (err, rows) {
        if (!err && rows.length != 0) {
            callback(true,rows);
        }else{
            callback(false,[]);
        }
    });
}

//find webtoon keywords by titleid
function find_keywords(title_id,callback){
    var keywords=new Array();
    var sqlquery = "SELECT * FROM keywords WHERE title_id=?";
    connection.query(sqlquery, title_id,function (err, rows) {
        if (!err && rows.length != 0) {
            for (var i=0;i<rows.length;i++){
                var keyword={
                    text: rows[i].keywords_content,
                    weight: rows[i].ranking,
                }
                //console.log(keyword)
                keywords.push(keyword);
            }

            //sort by ranking
            keywords.sort(function(a,b){return a.ranking <b.ranking});
            //console.log(keywords)
            callback(true, keywords);
        }else{
            callback(false,[]);
        }
    });
}

//find webtoon suggestions by titleid
function find_suggestions_request(title_id, callback){
    console.log("REQUEST")
    var sqlquery = "SELECT * FROM suggestions WHERE title_id_request=? ORDER BY dist LIMIT 15";
    connection.query(sqlquery, title_id,function (err, rows){
        if (!err && rows.length != 0) {
            console.log(rows);
           callback(rows)
        }else{
            callback([]);
        }
    });
}

function find_top_suggestions(title_id, callback){
    console.log("TOP 5")
    var list=new Array();
        find_suggestions_request(title_id,function(suggestions) {
                list=suggestions;
                var unique=new Array();
           for(var i=0;i<15;i++){
               var num=0;
               for(var j=0;j<unique.length;j++){
                   if(unique[j].title_id_suggestion==list[i].title_id_suggestion) {
                       num=-1;
                        break;
                   }
               }
               if(num==0){
                   unique.push(list[i]);
               }
           }
           console.log(unique);
           var res = new Array();//final result
            for (var j = 0; j < 6; j++) { //top 5
                find_webtoon(unique[j].title_id_suggestion, function (p, arr) {
                    if (p) {
                        res.push(arr[0])
                                }
                    })
                    if (j == 5) {
                        console.log(res);
                        callback(res);
                    }
            }
        })
}

//find webtoon hashtags by titleid
function find_hashtags(title_id,callback){
    var hashtags=new Array();
    var sqlquery = "SELECT * FROM hashtags WHERE title_id=?";
    connection.query(sqlquery, title_id,function (err, rows) {
        if (!err && rows.length != 0) {
            for (var i=0;i<rows.length;i++){
                var hashtag={
                    hashtag_id: rows[i].hashtags_id,
                    content: rows[i].contents,
                    ranking: rows[i].ranking,
                }
                console.log(hashtag)
                hashtags.push(hashtag);
            }
            //sort by ranking
            hashtags.sort(function(a,b){return a.ranking <b.ranking});
            //console.log(keywords)
            callback(true, hashtags);
        }else{
            callback(false,[]);
        }
    });
}

//search hashtag list by hashtag_contents
function search_hashtags(hashtag_contents, callback){
    var hashtags=new Array();
    var sqlquery = "SELECT * FROM hashtags WHERE contents LIKE '%"+hashtag_contents+"%';";
    connection.query(sqlquery,function (err, rows) {
        if (!err && rows.length != 0) {
            for (var i=0;i<rows.length;i++){
                var hashtag={
                    hashtag_id: rows[i].hashtags_id,
                    content: rows[i].contents,
                    ranking: rows[i].ranking,
                    title_id: rows[i].title_id
                }
                hashtags.push(hashtag);
            }
            console.log(hashtag)
            callback(true, hashtags);
        }else{
            console.log('error')
            callback(false,[]);
        }
    });
}


//search hashtag list by hashtag_content
router.get('/hashtag/:hashtag_content', function(req, res, next) {
    console.log("search hashtag")
    var hashtag_content=req.params.hashtag_content;
    console.log(hashtag_content);
    search_hashtags(hashtag_content, function(result, hashtags) {
        if(req.session.user_id) {
            res.render('webtoons/hashtag_search', {
                user_id: req.session.user_id,
                hashtags: hashtags,
            });
        }else{
            res.render('webtoons/hashtag_search', {
                user_id: -1,
                hashtags: hashtags,
            });
        }
    })
});

//search hashtag list by hashtag_content
router.post('/hashtags', function(req, res, next) {
    console.log("search hashtag")
    var hashtag_content=req.body.hashtag_content;
    console.log(hashtag_content);
    search_hashtags(hashtag_content, function(result, hashtags) {
        if(result) {
            if(req.session.user_id) {
                res.render('webtoons/hashtag_search', {
                    user_id: req.session.user_id,
                    hashtags: hashtags,
                });
            }else{
                res.render('webtoons/hashtag_search', {
                    user_id: -1,
                    hashtags: hashtags,
                });
            }
        }else{
            res.redirect('/');
        }
    })
});

/* GET webtoon page by title_id. */
router.get('/:title_id', function(req, res, next) {
    var title_id=req.params.title_id;
    console.log(title_id);
    find_webtoon(title_id,function(result, info){
        if(result){
            find_top_suggestions(title_id,function(list) {
                find_keywords(title_id, function (result, keywords) {
                    find_hashtags(title_id, function (result, hashtags) {
                        console.log("list"+list)
                        if(req.session.user_id){
                        res.render('webtoons/info', {
                            user_id: req.session.user_id,
                            info: info,
                            suggestions: list,
                            keywords: keywords,
                            hashtags: hashtags,
                            title_id: title_id
                        });
                            }else{
                            res.render('webtoons/info', {
                                user_id: -1,
                                info: info,
                                suggestions: list,
                                keywords: keywords,
                                hashtags: hashtags,
                                title_id: title_id
                            });
                        }
                    })
                })
            })

        }else{
            res.redirect('/');
        }
    })
});


module.exports = router;
