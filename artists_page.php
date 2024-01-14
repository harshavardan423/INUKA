<?php
   // Retrieve artist ID from the URL parameter
   $artistId = isset($_GET['artist_id']) ? $_GET['artist_id'] : null;

   // Use $artistId to fetch the corresponding artist information from a database or other source
   $artistInfo = getArtistInfoById($artistId);

   // Display the artist information on the page
?>
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title><?php echo $artistInfo['name']; ?> - Artist Page</title>
</head>
<body>
   <h1><?php echo $artistInfo['name']; ?></h1>
   <p><?php echo $artistInfo['bio']; ?></p>
   <!-- Add more content as needed -->

   <!-- You can include JavaScript for additional interactivity if required -->
</body>
</html>
