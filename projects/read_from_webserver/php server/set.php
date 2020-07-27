<?php

if(isset($_GET['name'])) {
        echo($_GET['name']);
        if(isset($_GET['data'])) {
                file_put_contents($_GET["name"].".dat",$_GET['data']);
                echo(', you put the following data <br/>'.$_GET['data']);

        }
}
?>
