// module
var createError = require("http-errors");
var express = require("express");
var path = require("path");
var session = require("express-session");
var cookieParser = require("cookie-parser");
var logger = require("morgan");
var favicon = require("serve-favicon");
var bodyParser = require("body-parser");
var mysql = require("mysql");
var request = require("request");
const SequelizeAuto = require("sequelize-auto");
var async = require("async");

//routing
var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
var webtoonsRouter = require('./routes/webtoons');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger("dev"));
app.use(bodyParser.json());
app.use(express.urlencoded({extended: false}));
app.use(cookieParser());
app.use(
    session({
      key: "sid", // 세션키
      secret: "secret", // 비밀키
      cookie: {
        maxAge: 1000 * 60 * 60 // 쿠키 유효기간 1시간
      }
    })
);
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/webtoons', webtoonsRouter);

server = {};
server.port = process.argv[2];
console.log(server);

app.listen(server.port, function(){
  console.log('node-rest-demo pid %s listening on %d', process.pid, server.port);
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : 'root',
  port     : 3306,
  database : 'bigdata'
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};
  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;