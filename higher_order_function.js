//-------------------------------------- Higher-Order Function--------------------------------------------c
function applyDiscount(products, discountFunction) {
  return products.map(product => {
    return {
      name: product.name,
      price: discountFunction(product.price)
    };
  });
}

function tenPercentOff(price) {
  return price - price * 0.10;
}

function twentyPercentOff(price) {
  return price - price * 0.20;
}


const products = [
  { name: "Laptop", price: 60000 },
  { name: "Mobile", price: 20000 },
  { name: "Headphones", price: 3000 }
];


const discountedProducts = applyDiscount(products, twentyPercentOff);

console.log(discountedProducts);