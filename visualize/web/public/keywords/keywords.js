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
var keywords=new Array();

fs.createReadStream('tf_idf_output2.csv')
    .pipe(csv())
    .on('data', (row) => {
        keywords.push(row);
    })
    .on('end', () => {
        console.log('CSV file successfully processed');
        keywords.forEach(function (keyword) {
            var sql = "INSERT INTO `keywords` (title_id, keywords_content, tf_idf, ranking) VALUES(?)";
            var values = [keyword.title_id, keyword.contents, keyword.td_idf, keyword.ranking];
            connection.query(sql, [values], function (err, result) {
                if (err) {
                    console.log("웹툰 DB 에러 : " + err);
                } else {
                    console.log("웹툰 DB처리 완료!");
                }
            });
        });
        console.log("FINISHed")
    });
console.log("DONE")