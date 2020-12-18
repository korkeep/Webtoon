var express = require('express');
var request = require('request');
var cheerio = require('cheerio');
var router = express.Router();
var mysql = require('mysql');

function crawling_webtoons(){
    var allWebtoonList=new Array();
    var allWeeklyToonsUrl = "http://comic.naver.com/webtoon/weekday.nhn";
    request(allWeeklyToonsUrl,function (err, res, html) {
        if(!err){
            var $ = cheerio.load(html);
            var p = Promise.resolve();
            var eachs = $(".thumb").each(function (i) {
                var week = $(this).parent().parent().prev().attr('class');
                var webtoon_link = "http://comic.naver.com" + $(this).children().first().attr('href');
                var thumb_link = $(this).children().first().children().first().attr('src');
                var name = $(this).next().text();
                var titleid = webtoon_link.split('?')[1].split('&')[0].split('=')[1];
                var webtoon= {
                    title_id: titleid,
                    name : name,
                    thum_link : thumb_link,
                    webtoon_link : webtoon_link,
                    week : week,
                };
                allWebtoonList.push(webtoon);
            });
            p.then(function() {
                i = 0;
                allWebtoonList.forEach(function (webtoon) {
                    var sql= "INSERT INTO `webtoons` (title_id, title_name, thum_link, webtoon_link, week) VALUES(?)";
                            var values=[webtoon.title_id, webtoon.name, webtoon.thum_link, webtoon.webtoon_link,webtoon.week];
                            connection.query(sql,[values],function(err,result){
                                if (err) {
                                    console.log("웹툰 DB 에러 : " + err);
                                } else {
                                    console.log("웹툰 DB처리 완료!");
                        }
                    });
                    //});
                })
            });
            console.log("done")
        }
    });
}

function get_all_webtoons(callback) {
    //naver webtoon
    var sqlquery = "SELECT * FROM webtoons;";
    connection.query(sqlquery, function (err, rows) {
        if (rows.length != 0) {
            console.log(rows.length)
            callback(true, rows);
            }
         else {
            console.log("get all webtoons failed");
            callback(false, []);
        }
    });
}

//home page
router.get('/', function (req, res, next) {
        get_all_webtoons( function(result,list) {
            if(result==true) {
                if(req.session.user_id) {
                    res.render('index2', {
                        title: "WEBTOON COMMENT ANALYSIS",
                        user_id: req.session.user_id,
                        list: list,
                    });
                }else{
                        res.render('index2', {
                            title: "WEBTOON COMMENT ANALYSIS",
                            user_id: req.session.user_id,
                            list: list,
                        });
                }
            }else{
                res.render('index2', {
                    title: "WEBTOON COMMENT ANALYSIS",
                    user_id: -1,
                    list:[],
                });
            }
        })
});

//get register
router.get('/register', function (req, res, next) {
    res.render('index/register', {
        title: "Sign up",
        user_id: -1,
    });
});

//post register
router.post('/register', function (req, res, next) {
    var user_id = req.body.user_id;
    var user_pw = req.body.user_pw;
    var user_name = req.body.user_name;
    console.log(user_id);
    var sqlquery = "SELECT * FROM users WHERE user_id = ?";
    connection.query(sqlquery, user_id, function (err, rows) {
        if (rows.length == 0) {
            var sql2 = "INSERT INTO users (user_id, user_pw, user_name) VALUES (?,?,?)";
            connection.query(sql2, [user_id, user_pw,user_name], function (err) {
                if (err) {
                    console.log("inserting user failed");
                    throw err;
                } else {
                    console.log("user inserted successfully");
                    res.redirect("/login");
                }
            })
        } else {
            console.log("이미 있는 ID, ID를 다시 입력해주세요!");
            res.redirect("/login");
            throw err;
        }
    });
});

//get login
router.get('/login', function (req, res, next) {
    if (req.session.user_id) {
        res.render('users/mypage', {
            title: "Home",
            user_id: req.session.user_id,
        });
    } else {
        res.render('index/login', {
            title: "Home",
            user_id: -1,
        });
    }
});

//post login
router.post('/login', function (req, res, next) {
    var user_id = req.body.user_id;
    var user_pw = req.body.user_pw;
    console.log(user_id);
    var sqlquery = "SELECT  * FROM users WHERE user_id = ?";
    connection.query(sqlquery, user_id, function (err, row) {
        if (err) {
            console.log("no match");
            res.redirect('/');
        } else {
            console.log(row);
            console.log(row.length);
            if (row.length != 0) {
                if(user_pw=row[0].user_pw){
                    console.log("user login successfully");
                    console.log(row[0].user_id);
                    req.session.user_id = row[0].user_id;
                    //redirect path according to user_type
                    res.redirect('/users');
                }else{
                    res.render('index/login', {
                        msg: "비밀번가 일치하지 않습니다."
                    });
                }
            } else {// no matching id
                res.render('index/login', {
                    msg: "아이디가 일치하지 않습니다."
                });
            }
        }
    });
});

//logout
router.get('/logout', function (req, res, next) {
    req.session.destroy();  // 세션 삭제
    res.clearCookie('sid'); // 세션 쿠키 삭제
    res.redirect('/');
});

//crawling_webtoons();

module.exports = router;
