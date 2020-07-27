<?php

if(isset($_GET['name'])) {
        readfile($_GET['name'].'.dat');
}
?>
