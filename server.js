const Hapi = require("hapi");
const server = new Hapi.Server();
const os = require("os");
var util = require("util");

// var mkdirp = require('mkdirp');
// var getDirName = require('path').dirname;

server.connection({
  host: "172.31.34.26",
  port: 3000
});

server.route({
  // method: "GET",
  // path: "/",
  // handler: function(request, reply) {
  //   reply("Hello");
  // }
  method: "POST",
  path: "/upload",
  config: {
    payload: {
      maxBytes: 209715200,
      output: "stream",
      parse: false
    },
    handler: function(request, reply) {
      var multiparty = require("multiparty");
      var fs = require("fs");
      var form = new multiparty.Form();
      var obj = { table: [] };
      // var size = '';
      // var fileName = '';
      //   form.on('part', function(part){
      //       if(!part.filename) return;
      //       size = part.byteCount;
      //       fileName = part.filename;
      //   });
      // form.on('file', function(name,file){
      //       console.log(1.path);
      //       console.log(__dirname);
      //       console.log('filename: ' + fileName);
      //       console.log('fileSize: '+ (size / 1024));
      //       var tmp_path = file.path
      //        console.log('tmp_path: ' +tmp_path);
      //       var target_path = '/uploads/user.mp4';
      //       console.log('target_path: ' + target_path);

      //       fs.renameSync(tmp_path, target_path, function(err) {
      //             if(err) console.error(err.stack);
      //       });
      //      // res.redirect('/uploads/fullsize/' + fileName);

      //   });
      form.parse(request.payload, function(err, fields, files) {
        console.log(err);
        console.log(fields);
        console.log(files);

        if (fs.existsSync("./record.json")) {
          fs.readFile("record.json", "utf8", function readFileCallback(
            err,
            data
          ) {
            if (err) {
              console.log(err);
            } else {
              obj = JSON.parse(data); //now it an object
              var finalobject = extend({}, fields, files);
              obj.table.push(finalobject);
              json = JSON.stringify(obj); //convert it back to json
              fs.writeFile("record.json", json, "utf8", function(err) {
                if (err) throw err;
                console.log("complete");
              }); // write it back
            }
          });
        } else {
          obj.table.push(fields); //add some data
          var finalobject = extend({}, fields, files);
          obj.table.push(finalobject);
          json = JSON.stringify(obj); //convert it back to json
          fs.writeFile("record.json", json, "utf8", function(err) {
            if (err) throw err;
            console.log("complete");
          }); // write it back
        }
      });
    }
  }
});

function extend(target) {
  var sources = [].slice.call(arguments, 1);
  sources.forEach(function(source) {
    for (var prop in source) {
      target[prop] = source[prop];
    }
  });
  return target;
}

server.start(function(err) {
  if (err) {
    throw err;
  }
  console.log("server started at: " + server.info.uri);
});
