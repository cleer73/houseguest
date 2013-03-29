<?php

$reps = rand(500, 1000);
$results = array();


try {
    // Connection
    $db = new PDO('mysql:host=localhost;dbname=benchmarks', 'root');

    // Build a query statement
    $query = $db->prepare('SELECT * FROM users WHERE id = :id');

    // Get a bunch of crap.
    for ($i=0; $i < $reps; $i++) {
        $query->execute(array(':id' => rand(1, 400000)));
        $results[] = $query->fetch(PDO::FETCH_ASSOC);
    }

    // Respond.
    json_response(array('count'=>count($results), 'data'=>$results));
} catch (PDOException $e) {
    json_response(array('message'=>'DATABASE FAILURE: '.$e->getMessage()));
}


function json_response($data) {
    header('Content-Type: application/json');
    exit(json_encode($data, JSON_NUMERIC_CHECK));
}