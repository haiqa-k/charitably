#<?php
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Charity Events & Causes Near Me</title>

    <!-- Bootstrap -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="page-header">
      <h1>CHARITABLY</h1>
      <p>Charity Events & Causes Near You</p>
  </div>
    <p><br/><br/></p>
    <div class="container">
      <table class="table table-bordered table-striped table-hover">
        <thead>
        <tr>
          <th>Name</th>
          <th>Start Date</th>
          <th>End Date</th>
          <th>Address</th> 
          <th>State</th>
          <th>Summary</th>
        </tr>

        <?php
        $conn = mysql_connect("localhost", "root", "myproject", "charitably");
        $sql = "SELECT * FROM Events";
        $result = $conn->($sql);

        if($result->num_rows > 0){
          while ($row = $result -> fetch_accos()){
            echo "<tr><td>" . $row["name"] . <tr><td>" . $row["start_date"] . <tr><td>" . $row["end_date"] . <tr><td>" . $row["street"] . <tr><td>" . $row["state"] . <tr><td>" . $row["description"]"
          }
        }
        else {
          echo "No Results";
        }
        $conn -> close();
        ?>
        </thead>
      </table>
    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  </body>
</html>