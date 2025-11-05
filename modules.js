// //expamle for the es6 module


// // export const PI = 3.14159;

// // export function add(a, b) {
// //   return a + b;
// // }

// // //example for the comman module in the javascript-----------------------------
 
// // function add(x, y) {
// //   return x + y;
// // }

// // const PI = 3.14;

// // // module.exports = { add, PI };


// // // example for the amcd module ---------------------------------
// // define(function() {
// //   return {
// //     add: function(x, y) { return x + y; },
// //     PI: 3.14
// //   };
// // });


// // AMD module example
// define(function() {
//   const PI = 3.14;

//   function add(a, b) {
//     return a + b;
//   }

//   function areaOfCircle(r) {
//     return PI * r * r;
//   }

//   // return makes these functions/values available to other files
//   return {
//     add,
//     areaOfCircle,        
//     PI
//   };
// });

let add = (num1, num2) => num1 + num2;
let sub = (num1, num2) => num1 - num2;
let mul = (num1, num2) => num1 * num2;
let div = (num1, num2) => num1 / num2;
let sqr = (num1) => num1 ** 2;
let cub = (num1) => num1 ** 3;

const abc = 30.22;

module.exports = { add, sub, mul, div, sqr, cub, abc };
