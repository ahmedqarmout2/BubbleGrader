var express = require('express');
var app = express();
const fileUpload = require('express-fileupload');
const https = require('https');
const fs = require('fs');
const bodyParser = require('body-parser');
const options = {
   key: fs.readFileSync(`${__dirname}/Keys/private.key`),
   cert: fs.readFileSync(`${__dirname}/Keys/cert.crt`)
};

app.use(fileUpload({
   limits: {
       fileSize: 50000
   },
   safeFileNames: true,
   preserveExtension: true,
   abortOnLimit: true
}));
app.use(bodyParser.urlencoded({
   limit: '50mb',
   extended: true
}));

app.use('/src', express.static(`${__dirname}/src`));

var server = app.listen(9081, function () {
   var host = server.address().address
   var port = server.address().port

   console.log("Example app listening at http://%s:%s", host, port);
});

const httpsServer = https.createServer(options, app);

httpsServer.listen(9082, function () {
   console.log('https on!');
});


app.get('/', function (req, res) {
   res.sendFile(__dirname + '/index.html');
});

app.post('/uploadImage', function (req, res) {
   console.log("got an image");
   const uploadedFile = req.body.imgBase64.replace(/^data:image\/png;base64,/, "");;
   fs.writeFile(__dirname + '/imgs/'+req.body.name, uploadedFile, 'base64', function (err) {
      if (err) {
         console.log(err);
         return res.status(200).send(JSON.stringify({'status':'ok'}));
      }
      return res.status(200).send("ok");
  });
});
