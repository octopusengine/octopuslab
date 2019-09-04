//---2015/07 - ing.Jan Copak --- octopusengine.org 
//================================================

var separator =" | ";
//

//----------------fibonaci--------------
function fibonaci(limit)
{
 var ret = "";
 var f1=0,f2=1,f3;
 var i;
 //alert("enter a text"+n);
 //var n=prompt("enter the number");
 //var n=20;

   for(i=2;i<=limit;i++)
   {
       f3=f1+f2;
       f1=f2;
       f2=f3;
     //document.write(f3+separator ); 
     ret = ret + f3+separator;  
   }
   //document.write("...");
   ret = ret + "..."; 
   document.getElementById("display").innerHTML = ret;
}


//----------------faktorial-------------
function faktorial(limit)
{
  var fact=1;
  for (i=1; i<limit; i++)
  {
  fact=fact*i;

  //document.write(i + "! = "+fact);
  document.write(fact);
  document.write(separator);
  }
  document.write("...");
}


//-------------- primes-----------------
function findPrimes(limit) {
  var ret = "";
  var primes = [], n, divisor;

  outerLoop: for( n = 2 ; n <= limit ; n++ ) {
    for( divisor = 2 ; divisor < n ; divisor++ ) {
      if( n % divisor === 0 ) {
        continue outerLoop;
      }
    }
    ///primes.push(n);
    //document.write(n);
    //document.write(separator);
    ret = ret + n + separator; 
  }

  ///return primes;
  ret = ret + "..."; 
  document.getElementById("display").innerHTML = ret;
} 




