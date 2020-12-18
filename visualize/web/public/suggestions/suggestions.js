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
var suggestions=new Array();

fs.createReadStream('distance.csv')
    .pipe(csv())
    .on('data', (row) => {
        suggestions.push(row);
    })
    .on('end', () => {
        console.log('CSV file successfully processed');
        var num=0;
        suggestions.forEach(function (suggest) {
            var sql = "INSERT INTO `suggestions` (title_id_request, title_id_suggestion, dist) VALUES(?)";
            var values = [ suggest.Title1,  suggest.Title2, suggest.Dist];
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