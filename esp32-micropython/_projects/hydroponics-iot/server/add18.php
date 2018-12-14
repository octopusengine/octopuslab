<?php
// 2018-02 esp - get>post
// $sql = "create table iot17 (id int, place varchar(8), device varchar(8), type varchar(8), value int, notice varchar(32), klic1 varchar(1), klic2 varchar(2), num3 int)";
// if($query = MySQL::query($sql)) echo  $sql."OK<br />"; 

                       
include_once 'my_db17.php';
include_once 'mysql_class.php';

$id = Date("U");
if (IsSet($_POST["value"])):$value=$_POST["value"];else:$value=0;endif;
if (IsSet($_POST["place"])):$place=$_POST["place"];else:$place="none";endif;
if (IsSet($_POST["device"])):$device=$_POST["device"];else:$device="id";endif;
if (IsSet($_POST["type"])):$type=$_POST["type"];else:$type="test";endif;
if (IsSet($_POST["version"])):$notice=$_POST["version"];else:$notice="";endif;
if (IsSet($_SERVER["HTTP_X_ESP8266_VERSION"])): $notice=substr($_SERVER["HTTP_X_ESP8266_VERSION"],0,12)." | ".$notice;endif;

if ($value <>0): $notice=""; endif;

//$value = $_GET['value'];
//$valuenum = $value/10;
//$type = $_GET['type'];
//$notice = $_GET['notice'];
//$notice = "...";

if(MySQL::connect($hostname, $uzivatel, $datpassw, $databaze)) {  //start
//---ok--- create table iot17 (id int, place varchar(8), device varchar(8), type varchar(8), value int, notice varchar(32), klic1 varchar(1), klic2 varchar(2), num3 int)
//---ok--- $sql =  "INSERT INTO test17 (id,value) VALUES ($id,$value)";
$sql =  "INSERT INTO iot17 (id,place,device,type,notice,value) VALUES ($id,'$place','$device','$type','$notice',$value)";
//echo  $sql; 
$query = MySQL::query($sql);
}
//
?>
