var express = require('express');
var router = express.Router();

//my fav webtoons list
function get_my_fav(user_id, callback){
  var sqlquery = "SELECT  w.title_id, w.title_name, w.thum_link, w.webtoon_link, w.week FROM fav f, webtoons w WHERE f.user_id = '"+user_id+"' &&  w.title_id=f.title_id;";
  var fav_list = new Array();
  connection.query(sqlquery,user_id,function(err,rows){
    if(!err){
      fav_list=rows;
      console.log(fav_list);
      callback(fav_list);
    }else{
      console.log("get my fav webtoon list failed!");
      //throw err;
      callback([]);
    }
  });
}

/* GET mypage. */
router.get('/', function(req, res, next) {
  if(!req.session.user_id){
    res.redirect('/');
  }else{
    console.log(req.session.user_id);
    get_my_fav(req.session.user_id, function (fav_list) {
       res.render('users/mypage', {
         user_id: req.session.user_id,
         fav_list: fav_list,
       });
    });
  }
});

//get webtoon list which aren't in my fav list
function get_webtoons_not_my_fav(user_id,callback) {
  get_my_fav(user_id,function(fav_list){
    var sqlquery = "SELECT * FROM webtoons";
    connection.query(sqlquery, function (err, rows) {
      if (rows.length != 0) {
        console.log("rows: ",rows.length);
        var webtoon_list=rows;
        for(var j=0;j<webtoon_list.length;j++) {
          for (var i = 0; i < fav_list.length; i++) {
           if(webtoon_list[j].title_id==fav_list[i].title_id){
             webtoon_list.splice(j,1);
           }
          }
        }
        console.log("filtered: ",webtoon_list.length);
        callback(true, webtoon_list)
      } else {
        console.log("get all webtoons failed");
        callback(false, []);
      }
    });
  })
}

//get add webtoon list page
router.get('/add', function(req, res, next) {
  var user_id=req.session.user_id;
  get_webtoons_not_my_fav(user_id,function(result, webtoon_list){
    if(result==true) {
      res.render('users/add_my_fav', {
        webtoon_list: webtoon_list
      });
    }else{
      res.redirect('/users')
    }
  });
});

//add webtoon to my fav list
function add_to_my_fav(user_id,title_id,callback){
  console.log(title_id);
  connection.query("INSERT INTO fav(user_id, title_id) VALUES(?,?);",
      [ user_id ,title_id] ,function (err) {
        if(err) {
          console.log("내 웹툰 추가중 에러!");
          callback(false)
        } else{
          callback(true)
        }
      });
}

//add to my fav list
router.post('/add',function(req,res,next){
  var title_id = req.body.title_id;
  var user_id = req.session.user_id;
  add_to_my_fav(user_id, title_id ,function(result){
    if(result==true){
      console.log("success");
      res.redirect('/users');
    }else{
      console.log("failed");
      res.redirect('/users');
    }
  })
});

function delete_webtoon_from_fav(user_id, title_id, callback){
  var sqlquery="DELETE FROM fav WHERE user_id='"+user_id+"'&& title_id='"+title_id+"';";
  connection.query(sqlquery, [user_id, title_id],function (err) {
        if(err) {
          throw err;
          console.log("내 웹툰 삭제중 에러!");
          callback(false)
        } else{
          callback(true)
        }
      });
}

//delete from my fav list
router.post('/delete',function(req,res,next){
  var title_id = req.body.title_id;
  var user_id = req.session.user_id;
  delete_webtoon_from_fav(user_id, title_id ,function(result){
    if(result==true){
      console.log("success");
      res.redirect('/users');
    }else{
      console.log("failed");
      res.redirect('/users');
    }
  })
});

module.exports = router;