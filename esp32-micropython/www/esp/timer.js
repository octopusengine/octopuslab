//=============================== timer ===========================
var interval = 500; 	//0,5 sec.
var interval2 = 5000; 	//5s
var c=1;
var t;
var timer_is_on=0;
var pointer = 0; 	//first is 1, "next" automaticaly
var pocet = 100; 	//interval of random numbers

function actionTimer(separator)
{
	//alert(separator );  
	document.getElementById('txt1').value=separator ;
	noiseM();
	drawM();
}

function timedCount()
{
  document.getElementById('txt2').value=c;

  var ch_nah = document.getElementById("chbx_nahod");
  zobrazovat_nahodne=ch_nah.checked;

  if(zobrazovat_nahodne) {nahoda = Math.round(Math.random() * (pocet-1)); 
	separator  = nahoda+1; 
	actionTimer(separator ); }
  else	{ doNext() }
  c=c+1;
  t=setTimeout("timedCount()",interval);
}


function doTimer()
{

if (!timer_is_on)
  {
  timer_is_on=1;
  timedCount();
  }
}

function doStop()
{
  clearTimeout(t);
  timer_is_on=0;
}

function doNext()
{
  separator ++;
  if (separator >pocet) separator  = 1;	
  actionTimer(separator );  
}

function doPrev()
{
  separator --;
  if (separator ==0) separator  = pocet;
  actionTimer(separator );  
}