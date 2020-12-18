const csv = require('csv-parser');
const fs = require('fs');
var mysql = require('mysql');

connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : 'root',
    port     : 3306,
    database : 'bigdata'
});
var hashtags=new Array();

fs.createReadStream('hashtag.csv')
    .pipe(csv())
    .on('data', (row) => {
        hashtags.push(row);
    })
    .on('end', () => {
        console.log('CSV file successfully processed');
        var num=0;
        hashtags.forEach(function (hashtag) {
            var sql = "INSERT INTO `hashtags` (title_id, contents, ranking) VALUES(?)";
            var values = [hashtag.id, hashtag.keyword,  hashtag.rank];
            connection.query(sql, [values], function (err, result) {
                if (err) {
                    console.log("웹툰 DB 에러 : " + err);
                } else {
                    num++;
                    console.log(num)
                    console.log("웹툰 DB처리 완료!");
                }
            });
        });
        console.log("FINISHed")
    });
console.log("DONE")