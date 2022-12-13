<?php

$TOKEN = "5651343058:AAEM0OVxht0AkvJk5RLQ4JJfm7dbuB0qawQ";
$TELEGRAM = "https://api.telegram.org:443/bot$TOKEN"; 

if (checkToken()) 
{  
  $request = receiveRequest();
  $chatId = $request->message->chat->id;
  $text = $request->message->text;

  $url = "https://top-cubist-365802.uc.r.appspot.com";
  $data = array('id' => $chatId, 'message' => $text);

  $options = array( 
    'http' => array(
      'header'  => "Content-type: application/x-www-form-urlencoded",
      'method'  => 'POST',
      'content' => http_build_query($data)
    )
  );
  $context  = stream_context_create($options);
  $resp = file_get_contents($url, false, $context);
  var_dump($resp);


  //sendMessage($chatId, "debug: " . $chatId  . " sent " . $text . " AppEngine respond: " . $resp);

}

function checkToken() 
{
  global $TOKEN;
  $pathInfo = ltrim($_SERVER['PATH_INFO'],'/');
  //echo $pathInfo;
  return $pathInfo == $TOKEN;
}

function receiveRequest() 
{
  $json = file_get_contents("php://input");
  $request = json_decode($json, $assoc=false);
  return $request;
}

function sendMessage($chatId, $text) 
{
  global $TELEGRAM;

  $query = http_build_query([
    'chat_id'=> $chatId,
    'text'=> $text,
    'parse_mode'=> "Markdown", 
  ]);

  $response = file_get_contents("$TELEGRAM/sendMessage?$query");
  return $response;
}
?>
