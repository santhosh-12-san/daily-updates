// --- ES6 Module Example ---
// export const PI = 3.14159;

// export function add(a, b) {
//   return a + b;
// }

// export function areaOfCircle(r) {
//   return PI * r * r;
// }



// --- CommonJS Module Example ---
// function add(a, b) {
//   return a + b;
// }

// function sub(a, b) {
//   return a - b;
// }

// const PI = 3.14;

// module.exports = { add, sub, PI };



// --- AMD Module Example ---
define(function() {
  const PI = 3.14;

  function add(a, b) {
    return a + b;
  }

  function areaOfCircle(r) {
    return PI * r * r;
  }

  return {
    add,
    areaOfCircle,
    PI
  };
});
