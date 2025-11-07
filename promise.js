// =------------------------------------------------------example for promise---------------------------------------------------------
// let p = new Promise((resolve, reject) => {
//   setTimeout(() => {
//     let asyncronus_function = false;

//     if (asyncronus_function) {
//       resolve("success");
//     } else {
//       reject("failure");
//     }
//   }, 2000);
// });

// p.then((res) => console.log(res))
//  .catch((err) => console.log(err));





// ------------------------------------------------------  swigguy exapmle--------------------------------------------------------------

// let swiggy = new Promise((res,rej)=>{
//     setTimeout(()=>{
//         let fun = true
//         if(fun){
//             res("accepted order")
//         }
//         else{
//             rej("out of stack")
//         }
//         },2000)
// })
// swiggy.then((resolve)=> console.log("resolved", resolve))
// .then(()=>console.log("your oder is reached shortly"))




 // --------------------------------------example for the  flase or reject -----------------------------------------------

// let swiggy = new Promise((res,rej)=>{
//     setTimeout(()=>{
//         let fun = false
//         if(fun){
//             res("accepted order")
//         }
//         else{
//             rej("out of stack")
//         }
//         },2000)
// })
// swiggy.then((resolve)=> console.log("resolved", resolve))
// .then(()=>console.log("your oder is reached shortly"))
// .catch((resolve)=>console.log("rejected",resolve))



      
// -----------------------------------------------example for the multiline promise----------------------------------------------------------------------------
// let p1 = Promise.resolve("food order")
// let p2 =new Promise((res,rej)=>{
//     res("order received!")
// //  rej("out of stack")
// })
// let p3 = new Promise((res,rej)=>{
//     setTimeout(()=>{
//         res("order deliverd")},5000)})

//         Promise.all([p1,p2,p3])
//         .then((results)=>console.log(results))
//         .catch((message)=>console.log(message))


    
// -----------------------------------------------example for  the race -------------------------------------------------------
// let p1 = Promise.resolve("food order")
// let p2 =new Promise((res,rej)=>{
//     res("order received!")
// //  rej("out of stack")
// })
// let p3 = new Promise((res,rej)=>{
//     setTimeout(()=>{
//         res("order deliverd")},5000)})

//         Promise.race([p1,p2,p3])
//         .then((results)=>console.log(results))
//         .catch((message)=>console.log(message))




// ---------------------------------------------------- example for the all ------------------------------------------------------------
// let p1 = Promise.resolve("food order")
// let p2 =new Promise((res,rej)=>{
//     res("order received!")
// //  rej("out of stack")
// })
// let p3 = new Promise((res,rej)=>{
//     setTimeout(()=>{
//         res("order deliverd")},5000)})

//         Promise.all([p1,p2,p3])
//         .then((results)=>console.log(results))
//         .catch((message)=>console.log(message))
    

// ---------------------------------------------------- example for the all settled ------------------------------------------------------------
// let p1 = Promise.resolve("food order")
// let p2 =new Promise((res,rej)=>{
//     res("order received!")
// //  rej("out of stack")
// })
// let p3 = new Promise((res,rej)=>{
//     setTimeout(()=>{
//         res("order deliverd")},5000)})

//         Promise.allSettled([p1,p2,p3])
//         .then((results)=>console.log(results))
//         .catch((message)=>console.log(message))
    
//---------------------------------------------------------------------- example for any-----------------------------------------------
let p1 = Promise.resolve("food order")
let p2 =new Promise((res,rej)=>{
    res("order received!")
//  rej("out of stack")
})
let p3 = new Promise((res,rej)=>{
    setTimeout(()=>{
        res("order deliverd")},5000)})

        Promise.any([p1,p2,p3])
        .then((results)=>console.log(results))
        .catch((message)=>console.log(message))
    
