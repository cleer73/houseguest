<?php

$reps = rand(1, 100);
$results = array();


try {
    $db = new PDO('mysql:host=localhost;dbname=benchmarks', 'root');

    $query = $db->prepare('SELECT * FROM users WHERE id = :id');

    for ($i=0; $i < $reps; $i++) {
        $query->execute(array(':id' => rand(1, 400000)));
        $results[] = $query->fetch(PDO::FETCH_ASSOC);
    }

    json_response($results);
} catch (PDOException $e) {
    json_response(array('message'=>'DATABASE FAILURE: '.$e->getMessage()));
}


function json_response($data) {
    header('Content-Type: application/json');
    print(json_encode($data, JSON_NUMERIC_CHECK));
}