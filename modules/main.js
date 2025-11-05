// Import from ES6 module
// import { PI, add, areaOfCircle } from './modules.js';

// console.log("PI:", PI);
// console.log("Add:", add(10, 5));
// console.log("Area of Circle:", areaOfCircle(5));




// --- CommonJS Module Example ---

// const { add, sub, PI } = require('./modules');

// console.log("PI:", PI);
// console.log("Add:", add(10, 5));
// console.log("Sub:", sub(10, 5));



// --- AMD Main File ---
require(['modules'], function(math) {
  console.log("PI:", math.PI);
  console.log("Add:", math.add(10, 5));
  console.log("Area of Circle:", math.areaOfCircle(5));
});
