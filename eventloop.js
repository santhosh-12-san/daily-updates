function func1(cd1,cd2,cd3){
    console.log('create order');
    cd1(cd2,cd3)
    
}
function func2(cd2,cd3){
    console.log('make the payment');
    cd2(cd3)

    
}
function func3(cd)
{
    setTimeout(()=>{
        console.log('deliver the order');
        cd()},3000)
        
    }
function func4(){
    console.log('eat');
    
}
func1(func2,func3,func4)




