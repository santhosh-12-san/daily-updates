// ------------------------------- e-commerce example--------------------------------------------------------
// function placeOrder() {
//     return new Promise(resolve => {
//         setTimeout(() => resolve("Order Placed"), 1000);
//     });
// }

// function processPayment() {
//     return new Promise(resolve => {
//         setTimeout(() => resolve("Payment Successful"), 1500);
//     });
// }

// function shipProduct() {
//     return new Promise(resolve => {
//         setTimeout(() => resolve("Product Shipped"), 2000);
//     });
// }

// placeOrder()
//   .then(res => {
//     console.log(res);
//     return processPayment();
//   })
//   .then(res => {
//     console.log(res);
//     return shipProduct();
//   })
//   .then(res => console.log(res))
//   .catch(err => console.log(err));


//--------------------------Manufacturing Industry--------------------------------------

// function getMachineStatus() {
//     return new Promise((resolve, reject) => {
//         setTimeout(() => {
//             let status = "RUNNING";  
//             resolve("Machine Status: " + status);
//         }, 2000);
//     });
// }

// getMachineStatus()
//     .then(data => console.log(data))
//     .catch(err => console.log(err));


//--------------------------------------banking -----------------------------

function fetchAccountDetails(accountId) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve({ accountId, balance: 50000, status: "Active" });
        }, 1500);
    });
}

fetchAccountDetails(101)
    .then(info => console.log(info))
    .catch(err => console.log(err));


