// example for the asyc and await 
// let p1 = new Promise((resolve, reject) => {
//   setTimeout(() => resolve("hello"), 3000);
// });

// async function executePromise() {
//   let response = await p1; // Await the promise here
//   console.log(response);
// }

// executePromise();
  


let p1 = new Promise((resolve, reject) => {
  setTimeout(() => resolve("hello1"), 1000);
});
let p2 = new Promise((resolve, reject) => {
  setTimeout(() => resolve("heelo2"), 2000);
});
let p3 = new Promise((resolve, reject) => {
  setTimeout(() => resolve("hello3"), 3000);
});
let p4 = new Promise((resolve, reject) => {
  setTimeout(() => resolve("hello4"), 4000);
});
let p5 = new Promise((resolve, reject) => {
  setTimeout(() => reject("hello5"), 5000);
});

async function executePromise() {
  let responses = await Promise.allSettled([p1, p2, p3, p4, p5]);
  console.log("All promises resolved:");
  console.log(responses);

  return responses;
}


executePromise()