// example for the read file ------------------------
// const fs = require('fs')
// let read_file = (file)=>{
//     fs.readFile(file,'utf8',(err,data)=>{
//         if(err){
//             console.error("error reading the file:",err);
//             return
//         }
//         console.log("file content");
//         console.log(data);
        
//     })
// }
// let file_name1 = "one1.txt"
// read_file(file_name1)

//write file ------------------------------------

// const fs = require('fs');

// let append_file = (file, contentToWrite) => {
//   fs.writeFile(file, contentToWrite, (err) => {
//     if (err) {
//       console.error(" Error writing to the file:", err);
//       return;
//     }
//     console.log(" File written successfully!");
//   });
// };

// let file_name2 = "two.txt";
// let some_content = "\n\nhappy morning";

// write_file(file_name2, some_content);


// append the file--------------------------------

// const fs = require('fs');

// let append_file = (file, contentToWrite) => {
//   fs.appendFile(file, contentToWrite, (err) => {
//     if (err) {
//       console.error(" Error writing to the file:", err);
//       return;
//     }
//     console.log(" File append file successfully!");
//   });
// };

// let file_name2 = "three.txt";
// let some_content = "\n\n helo happy morning";

// append_file(file_name2, some_content);




// delete the file ------------------------------------------------
const fs = require('fs');

let delete_file = (file) => {
  fs.unlink(file, (err) => {
    if (err) {
      console.error(" Error writing to the file:", err);
      return;
    }
    console.log(" File delete successfully!");
  });
};

let file_name2 = "four.txt";
delete_file(file_name2);