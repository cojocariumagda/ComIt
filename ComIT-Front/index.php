<?php
	$servername = 'localhost';
	$dbUsername = 'root';
	$dbPassword = 'Ceamaibunaparola1';
	$database = 'commIt';

	//connect to the database
	$conn = mysqli_connect($servername, $dbUsername, $dbPassword, $database);

	if($conn -> connect_error) {
		die("Conectarea la baza de date a esuat." . $conn -> connect_error);
	}

    function auth() {
	    $sql = "SELECT id FROM users WHERE logged = 1";

	    $statement = $GLOBALS['conn'] -> prepare($sql);
	    $statement -> execute();
	    $result = $statement->get_result();

	    if($result -> num_rows > 0) {
            echo '<script type="text/Javascript"> document.getElementById("auth").innerHTML = "Deconectare"; </script>';
            echo '<script type="text/Javascript"> document.getElementById("auth2").innerHTML = "Deconectare"; </script>';
        }
	    else {
	        echo '<script type="text/Javascript"> document.getElementById("auth").innerHTML = "Autentificare" </script>';
            echo '<script type="text/Javascript"> document.getElementById("auth2").innerHTML = "Autentificare"; </script>';
        }
    }

function login($numar) {
    if ($numar == 1) {
        $sql = "SELECT id FROM users WHERE logged = 1";
        $statement = $GLOBALS['conn']->prepare($sql);
        $statement->execute();
        $result = $statement->get_result();

        if (isset($_POST['uname']) && isset($_POST['psw'])) {

            $uname = $_POST['uname'];
            $psw = $_POST['psw'];

            if ($result->num_rows > 0) {
                $sql = "UPDATE users SET logged  = 0";
                $statement = $GLOBALS['conn']->prepare($sql);
                $statement->execute();
                auth();
                echo "V-ati deconectat.";


            }
            else {
                if($uname == "admin" && $psw == "admin") {
                    $sql = "UPDATE users SET logged = 1 WHERE uname = ?";
                    $statement = $GLOBALS['conn']->prepare($sql);
                    $statement->bind_param("s", $uname);
                    $statement->execute();
                    auth();
                    echo '<script> window.location.hash = "#admin"; </script>';
                }
                else {
                $sql = "SELECT id FROM users WHERE (uname = ?)";

                $statement = $GLOBALS['conn']->prepare($sql);
                $statement->bind_param("s", $uname);
                $statement->execute();

                $result = $statement->get_result();

                if ($result->num_rows > 0) {
                    $sql = "SELECT id FROM users WHERE (uname = ?) AND (psw = ?)";

                    $statement = $GLOBALS['conn']->prepare($sql);
                    $statement->bind_param("ss", $uname, $psw);
                    $statement->execute();

                    $result = $statement->get_result();

                    if ($result->num_rows > 0) {
                        echo 'Sunteti logat ca si ' . $uname . '.';

                        $sql = "UPDATE users SET logged = 1 WHERE uname = ?";
                        $statement = $GLOBALS['conn']->prepare($sql);
                        $statement->bind_param("s", $uname);
                        $statement->execute();
                        auth();
                    }
                    else {
                        echo "Parola gresita" . ".";
                    }
                }
                else {
                        echo "Nu exista acest utilizator.";
                }
                }
                $GLOBALS['conn']->close();
            }
        }
    }
    else {
        $sql = "SELECT id FROM users WHERE logged = 1";
        $statement = $GLOBALS['conn']->prepare($sql);
        $statement->execute();
        $result = $statement->get_result();

        if (isset($_POST['uname']) && isset($_POST['psw'])) {

            $uname = $_POST['uname'];
            $psw = $_POST['psw'];

            if ($result->num_rows > 0) {
                $sql = "UPDATE users SET logged  = 0 WHERE uname = ?";
                $statement = $GLOBALS['conn']->prepare($sql);
                $statement->bind_param("s", $uname);
                $statement->execute();

                auth();

            } else {
                $sql = "SELECT id FROM users WHERE (uname = ?)";

                $statement = $GLOBALS['conn']->prepare($sql);
                $statement->bind_param("s", $uname);
                $statement->execute();

                $result = $statement->get_result();

                if ($result->num_rows > 0) {
                    $sql = "SELECT id FROM users WHERE (uname = ?) AND (psw = ?)";

                    $statement = $GLOBALS['conn']->prepare($sql);
                    $statement->bind_param("ss", $uname, $psw);
                    $statement->execute();

                    $result = $statement->get_result();

                    if ($result->num_rows > 0) {

                        $sql = "UPDATE users SET logged = 1 WHERE uname = ?";
                        $statement = $GLOBALS['conn']->prepare($sql);
                        $statement->bind_param("s", $uname);
                        $statement->execute();
                        auth();
                    }
                }
                $GLOBALS['conn']->close();
            }
        }
    }
}

	function signIn() {
		if(isset($_POST['fname']) && isset($_POST['lname']) && isset($_POST['iuname']) && isset($_POST['ipsw'])) {
			$lname = $_POST['lname'];
			$fname = $_POST['fname'];
			$uname = $_POST['iuname'];
			$psw = $_POST['ipsw'];

			$sql = "SELECT uname FROM users WHERE uname = ?";

			$statement = $GLOBALS['conn'] -> prepare($sql);
			$statement -> bind_param("s", $uname);
			$statement -> execute();
			$result = $statement -> get_result();

			if($result -> num_rows > 0) {
				echo "Acest nume de utilizator nu este disponibil.";
			}
			else {

				if(isset($_POST['email'])) {

					$email = $_POST['email'];

					$sql = "INSERT INTO users (firstname, lastname, uname, psw, email, logged) VALUES (?, ?, ?, ?, ?, 1)";

					$statement = $GLOBALS['conn'] -> prepare($sql);
					$statement -> bind_param("sssss", $fname, $lname, $uname, $psw, $email);
					$result = $statement -> execute();


					if($result == FALSE) {
						echo "Ups. Nu am reusit sa introduc utilizatorul in baza de date. Va rugam sa incercati din nou.";
					}
					else {
					    auth();
                    }
				}
				else {

					$sql = "INSERT INTO users (firstname, lastname, uname, psw) VALUES (?, ?, ?, ?)";

					$statement = $GLOBALS['conn'] -> prepare($sql);
					$statement -> bind_param("ssss", $fname, $lname, $uname, $psw);
					$result = $statement -> execute();


                    if($result == FALSE) {
                        echo "Ups. Nu am reusit sa introduc utilizatorul in baza de date. Va rugam sa incercati din nou.";
                    }
                    else {
                        auth();
                    }
				}
			}
		}
	}

	function showEverything() {

		$sql = "SELECT * FROM users";

		$result = $GLOBALS['conn'] -> query($sql);

		if($result -> num_rows > 0) {
			while($row = $result -> fetch_assoc()) {
				echo $row['id'] . " " . $row['uname'] . " " . $row['psw'] . "<br>";
			}
		}
		else {
			echo "Nu sunt inregistrari in baza de date";
		}
	}

?>

<!DOCTYPE html>
<html lang = "ro">
	<head>
		<title> Compare It </title>
		<meta charset="utf-8">
		<meta name = "description" content = "Proiect TW">
		<meta name = "author" content = "Cernovschi Ioan Valentin, Cojocariu Magda">
		<meta name = "owner" content = "Cenovschi Ioan Valentin, Cojocariu Magda">
		<meta name = "keywords" content = "tw, web, project, infoiasi, pret, compara, produs, telefon, tableta, pc, laptop, monitor, calculator, carte, Cernovschi Ioan Valentin, Cojocariu Magda">
		<meta name = "viewport" content = "width=device-width, initial-scale = 1.0">
		<meta name = "distribution" content = "Global">
		<link rel = "stylesheet" type = "text/css" href = "CSS/stilIndex.css?d=<?php echo time(); ?>" />
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
	</head>
	<body>
		<div id = "header">
			<ul>
				<li><a href = "#about" id = "aHover"><img class = "logo-replacement" src = "./Imagini/compara.png" alt = "balanta"></a></li>
				<li><h1> Compare It </h1></li>
				<li>
					<input name = "bar" id = "searchBar" type = "text" placeholder="Puteti gasi produse la cele mai bune preturi de pe piata..." >
					<button name = "button" onclick="get()" id = "buttonA"><i class = "fa fa-search"></i></button>
				</li>
			</ul>
		</div>
        <script>
            function get() {
                const Http = new XMLHttpRequest();
                const url = "https://comittw.herokuapp.com/search_product?content_search=" + document.getElementById('searchBar').value;
                document.getElementById('searchBar').value = '';
                Http.open("GET", url);
                Http.send();

                Http.onreadystatechange= (e) => {
                    const result = JSON.parse(Http.responseText);
                    parseResult(result);
                };
            }

            function parseResult(result) {
                var out = "";
                var i;
                for(i = 0; i < result.length; i++) {
                    out += '<div class = "produs"><a target = "_blank" href="' + result[i].link_produs + '">' +
                        '<img class = "imagine_produs" src ="' + result[i].imagine_produs + '"' +
                        ' alt = "imagine produs" > ' + '</a><span class = "nextToImage">' + result[i].nume_produs +
                        '<br>' + 'Pret: ' + convert(result[i].pret_produs) + '<br>' +
                        'Rating: ' + result[i].rating_produs + '<br>' +
                        'Valabilitate: ' + result[i].valabilitate_produs + '<br>' + '</span></div><br>';
                }
                document.getElementById("searchTarget").innerHTML = out;
                window.location.hash = '#searchTarget';
            }
        </script>

        <div class="navbar">
            <div class="dropdown">
                <button class="dropbtn">
                 <img class = "logo" src = "Imagini/emag.png">
                </button>
                <div class="dropdown-content">
                    <a class = "dropbtnSecond" onclick="emagNews()" href = "#xml"><span class = "rss">View RSS Feed</span></a>
                    <div class ="dropdownSecond">
                       <a class = "dropbtnSecond" onclick="getEmagCategory('Laptop, Tablete %26 Telefoane')" href="#produse">Laptop, Tablete & Telefoane</a></button>
                        <div class = "dropdown-content-second">
                            <a onclick="getEmagSubcategory('Tablete si accesorii')" href = "#produse">Tablete si accesorii</a>
                            <a onclick="getEmagSubcategory('Laptopuri si accesorii')" href = "#produse">Laptopuri si accesorii</a>
                            <a onclick="getEmagSubcategory('Telefoane mobile si accesorii')" href = "#produse">Telefoane mobile si accesorii</a>
                            <a onclick="getEmagSubcategory('Wearables %26 Gadgeturi')" href = "#produse">Wearables &amp; Gadgeturi</a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEmagCategory('PC, Periferice %26 Software')" class = "dropbtnSecond" href="#produse">PC, Periferice &amp; Software</a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEmagSubcategory('Tablete si accesorii')" href = "#produse">Retelistica &amp; supraveghere</a>
                            <a onclick="getEmagSubcategory('Periferice PC')" href = "#produse">Periferice PC</a>
                            <a onclick="getEmagSubcategory('Componente PC')" href = "#produse">Componente PC</a>
                            <a onclick="getEmagSubcategory('Servere, Componente %26 UPS')" href = "#produse">Servere, Componente &amp; UPS</a>
                            <a onclick="getEmagSubcategory('Imprimante, scanere %26 consumabile')" href = "#produse">Imprimante, scanere &amp; consumabile</a>
                            <a onclick="getEmagSubcategory('Desktop PC %26 Monitoare')" href = "#produse">Desktop PC &amp; Monitoare</a>
                            <a onclick="getEmagSubcategory('Software')" href = "#produse">Software</a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEmagCategory('TV, Audio-Video %26 Foto')" class = "dropbtnSecond" href="#produse">TV, Audio-Video &amp; Foto</a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEmagSubcategory('Camere video sport %26 accesorii')" href = "#produse">Camere video sport &amp; accesorii</a>
                            <a onclick="getEmagSubcategory('Aparate foto %26 accesorii')"href = "#produse">Aparate foto &amp; accesorii</a>
                            <a onclick="getEmagSubcategory('Home Cinema %26 Audio')"href = "#produse">Home Cinema &amp; Audio</a>
                            <a onclick="getEmagSubcategory('Audio HI-FI %26 Profesionale')"href = "#produse">Audio HI-FI &amp; Profesionale</a>
                            <a onclick="getEmagSubcategory('Televizoare %26 accesorii')"href = "#produse">Televizoare &amp; accesorii</a>
                            <a onclick="getEmagSubcategory('Drone si accesorii')"href = "#produse">Drone si accesorii</a>
                            <a onclick="getEmagSubcategory('Videoproiectoare %26 accesorii')"href = "#produse">Videoproiectoare &amp; accesorii</a>
                            <a onclick="getEmagSubcategory('Portabile audio')"href = "#produse">Portabile audio</a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEmagCategory('Electrocasnice %26 Climatizare')" class = "dropbtnSecond" href="#produse">Electrocasnice &amp; Climatizare</a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEmagSubcategory('Aparate de aer conditionat')" href = "#produse">Aparate de aer conditionat</a>
                            <a onclick="getEmagSubcategory('Aspiratoare %26 fiare de calcat')" href = "#produse">Aspiratoare &amp; fiare de calcat</a>
                            <a onclick="getEmagSubcategory('Aragazuri, hote si cuptoare')" href = "#produse">Aragazuri, hote si cuptoare</a>
                            <a onclick="getEmagSubcategory('Electrocasnice bucatarie')" href = "#produse">Electrocasnice bucatarie</a>
                            <a onclick="getEmagSubcategory('Incorporabile')" href = "#produse">Incorporabile</a>
                            <a onclick="getEmagSubcategory('Masini de spalat vase')" href = "#produse">Masini de spalat vase</a>
                            <a onclick="getEmagSubcategory('Masini de spalat rufe')" href = "#produse">Masini de spalat rufe</a>
                            <a onclick="getEmagSubcategory('Climatizare')" href = "#produse">Climatizare</a>
                            <a onclick="getEmagSubcategory('Aparate frigorifice')" href = "#produse">Aparate frigorifice</a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEmagCategory('Bacanie')" class = "dropbtnSecond" href="#produse">Bacanie</a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEmagSubcategory('Produse dezinfectante')" href = "#produse">Produse dezinfectante</a>
                            <a onclick="getEmagSubcategory('Bauturi alcoolice')" href = "#produse">Bauturi alcoolice</a>
                            <a onclick="getEmagSubcategory('Cosmetice')" href = "#produse">Cosmetice</a>
                            <a onclick="getEmagSubcategory('Bacanie')" href = "#produse">Bacanie</a>
                            <a onclick="getEmagSubcategory('Spalare %26 intretinere rufe')" href = "#produse">Spalare &amp; intretinere rufe</a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEmagCategory('Fashion')" class = "dropbtnSecond" href="#produse">Fashion</a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEmagSubcategory('Genti si accesorii barbati')" href = "#produse">Genti si accesorii barbati</a>
                            <a onclick="getEmagSubcategory('Genti si accesorii femei')" href = "#produse">Genti si accesorii femei</a>
                            <a onclick="getEmagSubcategory('Imbracaminte barbati')" href = "#produse">Imbracaminte barbati</a>
                            <a onclick="getEmagSubcategory('Incaltaminte femei')" href = "#produse">Incaltaminte femei</a>
                            <a onclick="getEmagSubcategory('Incaltaminte barbati')" href = "#produse">Incaltaminte barbati</a>
                            <a onclick="getEmagSubcategory('Imbracaminte femei')" href = "#produse">Imbracaminte femei</a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEmagCategory('Ingrijire personala %26 Cosmetice')" class = "dropbtnSecond" href="#produse">Ingrijire personala &amp; Cosmetice</a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEmagSubcategory('Cosmetice %26 Ingrijire personala')" href = "#produse">Cosmetice &amp; Ingrijire personala</a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEmagCategory('Casa, Gradina %26 Bricolaj')" class = "dropbtnSecond" href="#produse">Casa, Gradina &amp; Bricolaj</a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEmagSubcategory('Textile %26 covoare')" href = "#produse">Textile &amp; covoare</a>
                            <a onclick="getEmagSubcategory('Mobilier de gradina')" href = "#produse">Mobilier de gradina</a>
                            <a onclick="getEmagSubcategory('Gradinarit')" href = "#produse">Gradinarit</a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEmagCategory('Sport %26 Activitati in aer liber')" class = "dropbtnSecond" href="#produse">Sport &amp; Activitati in aer liber</a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEmagSubcategory('Incaltaminte sport')" href = "#produse">Incaltaminte sport</a>
                            <a onclick="getEmagSubcategory('Imbracaminte sport')" href = "#produse">Imbracaminte sport</a>
                            <a onclick="getEmagSubcategory('Fitness si nutritie')" href = "#produse">Fitness si nutritie</a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEmagCategory('Auto, Moto %26 RCA')" class = "dropbtnSecond" href="#produse">Auto, Moto  &amp; RCA</a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEmagSubcategory('Anvelope %26 Jante')" href = "#produse">Anvelope &amp; Jante</a>
                            <a onclick="getEmagSubcategory('Eletronice Auto')" href = "#produse">Eletronice Auto</a>
                            <a onclick="getEmagSubcategory('Accesorii auto')" href = "#produse">Accesorii auto</a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEmagCategory('Jucarii, Copii %26 Bebe')" class = "dropbtnSecond" href="#produse">Jucarii, Copii &amp; Bebe</a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEmagSubcategory('Bebelusi')" href = "#produse">Bebelusi</a>
                        </div> </div>

                </div>
            </div>
            <div class="dropdown">
                <button class="dropbtn">
                    <img class = "logo" src = "Imagini/evomag.png">
                </button>
                <div class="dropdown-content">
                    <a class = "dropbtnSecond" onclick="evomagNews()" href = "#xml"><span class = "rss">View RSS Feed</span></a>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Laptopuri si Tablete')" class = "dropbtnSecond" href="#produse"> Laptopuri si Tablete </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory(' Laptopuri %2F Notebook ')" href = "#produse"> Laptopuri / Notebook </a>
                            <a onclick="getEvomagSubcategory('Tablete ')" href = "#produse">Tablete </a>
                            <a onclick="getEvomagSubcategory('Huse Tablete ')" href = "#produse">Huse Tablete </a>
                            <a onclick="getEvomagSubcategory('Folii Protectie Tablete ')" href = "#produse">Folii Protectie Tablete </a>
                            <a onclick="getEvomagSubcategory('Stylus Pen ')" href = "#produse">Stylus Pen </a>
                            <a onclick="getEvomagSubcategory('eBook Readere ')" href = "#produse">eBook Readere </a>
                            <a onclick="getEvomagSubcategory('Alte accesorii laptop-uri ')" href = "#produse">Alte accesorii laptop-uri </a>
                            <a onclick="getEvomagSubcategory('Accesorii mac ')" href = "#produse">Accesorii mac </a>
                            <a onclick="getEvomagSubcategory('Extindere garantie ')" href = "#produse">Extindere garantie </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Telefoane mobile si Accesorii')" class = "dropbtnSecond" href="#produse"> Telefoane mobile si Accesorii </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Telefoane mobile ')" href = "#produse">Telefoane mobile </a>
                            <a onclick="getEvomagSubcategory('Casti bluetooth, airpods si audio ')" href = "#produse">Casti bluetooth, airpods si audio </a>
                            <a onclick="getEvomagSubcategory('Boxe Portabile cu Bluetooth ')" href = "#produse">Boxe Portabile cu Bluetooth </a>
                            <a onclick="getEvomagSubcategory('Incarcatoare ')" href = "#produse">Incarcatoare </a>
                            <a onclick="getEvomagSubcategory('Smartwatch ')" href = "#produse">Smartwatch </a>
                            <a onclick="getEvomagSubcategory('Telefoane Seniori ')" href = "#produse">Telefoane Seniori </a>
                            <a onclick="getEvomagSubcategory('Telefoane Fixe ')" href = "#produse">Telefoane Fixe </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('TV %26 Multimedia')" class = "dropbtnSecond" href="#produse"> TV & Multimedia </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('LED TV ')" href = "#produse">LED TV </a>
                            <a onclick="getEvomagSubcategory('Sistem Home Cinema ')" href = "#produse">Sistem Home Cinema </a>
                            <a onclick="getEvomagSubcategory('Soundbar ')" href = "#produse">Soundbar </a>
                            <a onclick="getEvomagSubcategory('Sisteme Audio ')" href = "#produse">Sisteme Audio </a>
                            <a onclick="getEvomagSubcategory('Player Multimedia ')" href = "#produse">Player Multimedia </a>
                            <a onclick="getEvomagSubcategory('Centrale Home Center ')" href = "#produse">Centrale Home Center </a>
                            <a onclick="getEvomagSubcategory('Prize inteligente ')" href = "#produse">Prize inteligente </a>
                            <a onclick="getEvomagSubcategory('Senzori si Detectoare ')" href = "#produse">Senzori si Detectoare </a>
                            <a onclick="getEvomagSubcategory('Accesorii tablete grafice ')" href = "#produse">Accesorii tablete grafice </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Componente PC %26amp; Gaming')" class = "dropbtnSecond" href="#produse"> Componente PC &amp; Gaming </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Placi Video ')" href = "#produse">Placi Video </a>
                            <a onclick="getEvomagSubcategory('Solid-State Drive ')" href = "#produse">Solid-State Drive </a>
                            <a onclick="getEvomagSubcategory('Procesoare ')" href = "#produse">Procesoare </a>
                            <a onclick="getEvomagSubcategory('Placi de baza ')" href = "#produse">Placi de baza </a>
                            <a onclick="getEvomagSubcategory('Jocuri Video - PC si Consola ')" href = "#produse">Jocuri Video - PC si Consola </a>
                            <a onclick="getEvomagSubcategory('Console ')" href = "#produse">Console </a>
                            <a onclick="getEvomagSubcategory('Accesorii console ')" href = "#produse">Accesorii console </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Calculatoare - Sisteme PC')" class = "dropbtnSecond" href="#produse"> Calculatoare - Sisteme PC </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('All In One PC ')" href = "#produse">All In One PC </a>
                            <a onclick="getEvomagSubcategory('Calculatoare desktop ')" href = "#produse">Calculatoare desktop </a>
                            <a onclick="getEvomagSubcategory('Calculatoare Refurbished ')" href = "#produse">Calculatoare Refurbished </a>
                            <a onclick="getEvomagSubcategory('Servere ')" href = "#produse">Servere </a>
                            <a onclick="getEvomagSubcategory('Procesoare Server ')" href = "#produse">Procesoare Server </a>
                            <a onclick="getEvomagSubcategory('Placi de baza Server ')" href = "#produse">Placi de baza Server </a>
                            <a onclick="getEvomagSubcategory('Memorii Server ')" href = "#produse">Memorii Server </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Monitoare')" class = "dropbtnSecond" href="#produse"> Monitoare </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Monitoare LED ')" href = "#produse">Monitoare LED </a>
                            <a onclick="getEvomagSubcategory('Accesorii Monitoare ')" href = "#produse">Accesorii Monitoare </a>
                            <a onclick="getEvomagSubcategory('Monitoare Refurbished ')" href = "#produse">Monitoare Refurbished </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Electrocasnice')" class = "dropbtnSecond" href="#produse"> Electrocasnice </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Aparate frigorifice ')" href = "#produse">Aparate frigorifice </a>
                            <a onclick="getEvomagSubcategory('Frigidere ')" href = "#produse">Frigidere </a>
                            <a onclick="getEvomagSubcategory('Combine frigorifice ')" href = "#produse">Combine frigorifice </a>
                            <a onclick="getEvomagSubcategory('Congelatoare ')" href = "#produse">Congelatoare </a>
                            <a onclick="getEvomagSubcategory('Cuptoare incorporabile ')" href = "#produse">Cuptoare incorporabile </a>
                            <a onclick="getEvomagSubcategory('Aragazuri ')" href = "#produse">Aragazuri </a>
                            <a onclick="getEvomagSubcategory('Aspiratoare cu sac ')" href = "#produse">Aspiratoare cu sac </a>
                            <a onclick="getEvomagSubcategory('Aspiratoare fara sac ')" href = "#produse">Aspiratoare fara sac </a>
                            <a onclick="getEvomagSubcategory('Aspiratoare robot ')" href = "#produse">Aspiratoare robot </a>
                            <a onclick="getEvomagSubcategory('Cafetiere ')" href = "#produse">Cafetiere </a>
                            <a onclick="getEvomagSubcategory('Espressoare ')" href = "#produse">Espressoare </a>
                            <a onclick="getEvomagSubcategory('Rasnite ')" href = "#produse">Rasnite </a>
                            <a onclick="getEvomagSubcategory('Masini de facut paine ')" href = "#produse">Masini de facut paine </a>
                            <a onclick="getEvomagSubcategory('Multicooker ')" href = "#produse">Multicooker </a>
                            <a onclick="getEvomagSubcategory('Slow cookere ')" href = "#produse">Slow cookere </a>
                            <a onclick="getEvomagSubcategory('Dezumidificatoare ')" href = "#produse">Dezumidificatoare </a>
                            <a onclick="getEvomagSubcategory('Umidificatoare ')" href = "#produse">Umidificatoare </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Imprimante')" class = "dropbtnSecond" href="#produse"> Imprimante </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Multifunctionale ')" href = "#produse">Multifunctionale </a>
                            <a onclick="getEvomagSubcategory('Consumabile ')" href = "#produse">Consumabile </a>
                            <a onclick="getEvomagSubcategory('Imprimante laser alb-negru ')" href = "#produse">Imprimante laser alb-negru </a>
                            <a onclick="getEvomagSubcategory('Imprimante laser color ')" href = "#produse">Imprimante laser color </a>
                            <a onclick="getEvomagSubcategory('Imprimante jet cerneala ')" href = "#produse">Imprimante jet cerneala </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Foto')" class = "dropbtnSecond" href="#produse"> Foto </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Carduri memorie ')" href = "#produse">Carduri memorie </a>
                            <a onclick="getEvomagSubcategory('Aparate Foto Compacte ')" href = "#produse">Aparate Foto Compacte </a>
                            <a onclick="getEvomagSubcategory('Rame Digitale ')" href = "#produse">Rame Digitale </a>
                            <a onclick="getEvomagSubcategory('Obiective ')" href = "#produse">Obiective </a>
                            <a onclick="getEvomagSubcategory('Binocluri ')" href = "#produse">Binocluri </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Video')" class = "dropbtnSecond" href="#produse"> Video </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Supraveghere video ')" href = "#produse">Supraveghere video </a>
                            <a onclick="getEvomagSubcategory('Videoproiectoare ')" href = "#produse">Videoproiectoare </a>
                            <a onclick="getEvomagSubcategory('Camere Video ')" href = "#produse">Camere Video </a>
                            <a onclick="getEvomagSubcategory('Accesorii camere video pentru sporturi extreme ')" href = "#produse">Accesorii camere video pentru sporturi extreme </a>
                            <a onclick="getEvomagSubcategory('Acumulatori Video ')" href = "#produse">Acumulatori Video </a>
                            <a onclick="getEvomagSubcategory('Genti Video ')" href = "#produse">Genti Video </a>
                            <a onclick="getEvomagSubcategory('Ecrane de proiectie ')" href = "#produse">Ecrane de proiectie </a>
                            <a onclick="getEvomagSubcategory('Table interactive ')" href = "#produse">Table interactive </a>
                            <a onclick="getEvomagSubcategory('Alte Accesorii Proiector ')" href = "#produse">Alte Accesorii Proiector </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Software')" class = "dropbtnSecond" href="#produse"> Software </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Sisteme operare PC ')" href = "#produse">Sisteme operare PC </a>
                            <a onclick="getEvomagSubcategory('Aplicatii ')" href = "#produse">Aplicatii </a>
                            <a onclick="getEvomagSubcategory('Antivirusi ')" href = "#produse">Antivirusi </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Retelistica')" class = "dropbtnSecond" href="#produse"> Retelistica </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Routere ')" href = "#produse">Routere </a>
                            <a onclick="getEvomagSubcategory('Access point ')" href = "#produse">Access point </a>
                            <a onclick="getEvomagSubcategory('Extendere Wi-Fi ')" href = "#produse">Extendere Wi-Fi </a>
                            <a onclick="getEvomagSubcategory('Switch-uri ')" href = "#produse">Switch-uri </a>
                            <a onclick="getEvomagSubcategory('Network Attached Storage ')" href = "#produse">Network Attached Storage </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('AUTO')" class = "dropbtnSecond" href="#produse"> AUTO </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Camere Video Auto ')" href = "#produse">Camere Video Auto </a>
                            <a onclick="getEvomagSubcategory('Lazi frigorifice ')" href = "#produse">Lazi frigorifice </a>
                            <a onclick="getEvomagSubcategory('Frigidere Auto ')" href = "#produse">Frigidere Auto </a>
                            <a onclick="getEvomagSubcategory('Statii auto ')" href = "#produse">Statii auto </a>
                            <a onclick="getEvomagSubcategory('Covorase Auto ')" href = "#produse">Covorase Auto </a>
                            <a onclick="getEvomagSubcategory('Stergatoare ')" href = "#produse">Stergatoare </a>
                            <a onclick="getEvomagSubcategory('Senzori de parcare ')" href = "#produse">Senzori de parcare </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Ingrijire personala')" class = "dropbtnSecond" href="#produse"> Ingrijire personala </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Tensiometre ')" href = "#produse">Tensiometre </a>
                            <a onclick="getEvomagSubcategory('Termometre ')" href = "#produse">Termometre </a>
                            <a onclick="getEvomagSubcategory('Glucometre ')" href = "#produse">Glucometre </a>
                            <a onclick="getEvomagSubcategory('Epilatoare ')" href = "#produse">Epilatoare </a>
                            <a onclick="getEvomagSubcategory('Epilatoare IPL ')" href = "#produse">Epilatoare IPL </a>
                            <a onclick="getEvomagSubcategory('Aparate de tuns ')" href = "#produse">Aparate de tuns </a>
                            <a onclick="getEvomagSubcategory('Aparate de ras electrice ')" href = "#produse">Aparate de ras electrice </a>
                            <a onclick="getEvomagSubcategory('Aparate de tuns barba ')" href = "#produse">Aparate de tuns barba </a>
                            <a onclick="getEvomagSubcategory('Periute de dinti electrice ')" href = "#produse">Periute de dinti electrice </a>
                            <a onclick="getEvomagSubcategory('Irigatoare bucale si accesorii pentru dusul bucal ')" href = "#produse">Irigatoare bucale si accesorii pentru dusul bucal </a>
                            <a onclick="getEvomagSubcategory('Rezerve periute ')" href = "#produse">Rezerve periute </a>
                            <a onclick="getEvomagSubcategory('Uscatoare de par ')" href = "#produse">Uscatoare de par </a>
                            <a onclick="getEvomagSubcategory('Placi de indreptat parul ')" href = "#produse">Placi de indreptat parul </a>
                            <a onclick="getEvomagSubcategory('Ondulatoare ')" href = "#produse">Ondulatoare </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Sport %26amp; Fitness')" class = "dropbtnSecond" href="#produse"> Sport &amp; Fitness </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Biciclete Electrice ')" href = "#produse">Biciclete Electrice </a>
                            <a onclick="getEvomagSubcategory('Trotinete Electrice ')" href = "#produse">Trotinete Electrice </a>
                            <a onclick="getEvomagSubcategory('Hoverboard ')" href = "#produse">Hoverboard </a>
                            <a onclick="getEvomagSubcategory('Bratari Fitness %26amp; Ceasuri Sportive ')" href = "#produse">Bratari Fitness &amp; Ceasuri Sportive </a>
                            <a onclick="getEvomagSubcategory('Accesorii gadgeturi pentru monitorizare activitate ')" href = "#produse">Accesorii gadgeturi pentru monitorizare activitate </a>
                            <a onclick="getEvomagSubcategory('Cantare de baie ')" href = "#produse">Cantare de baie </a>
                            <a onclick="getEvomagSubcategory('Biciclete ')" href = "#produse">Biciclete </a>
                            <a onclick="getEvomagSubcategory('Piese Biciclete si Accesorii ')" href = "#produse">Piese Biciclete si Accesorii </a>
                            <a onclick="getEvomagSubcategory('Trotinete si Triciclete ')" href = "#produse">Trotinete si Triciclete </a>
                            <a onclick="getEvomagSubcategory('Biciclete Fitness - Magntice %26amp; Eliptice ')" href = "#produse">Biciclete Fitness - Magntice &amp; Eliptice </a>
                            <a onclick="getEvomagSubcategory('Benzi de alergat ')" href = "#produse">Benzi de alergat </a>
                            <a onclick="getEvomagSubcategory('Steppere pentru Fitness ')" href = "#produse">Steppere pentru Fitness </a>
                            <a onclick="getEvomagSubcategory('Aparate Fitness Multifunctionale ')" href = "#produse">Aparate Fitness Multifunctionale </a>
                            <a onclick="getEvomagSubcategory('Aparate de vaslit ')" href = "#produse">Aparate de vaslit </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Mama si Copilul')" class = "dropbtnSecond" href="#produse"> Mama si Copilul </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Masti de protectie faciala ')" href = "#produse">Masti de protectie faciala </a>
                            <a onclick="getEvomagSubcategory('Sterilizatoare si accesorii ')" href = "#produse">Sterilizatoare si accesorii </a>
                            <a onclick="getEvomagSubcategory('Cantare ')" href = "#produse">Cantare </a>
                            <a onclick="getEvomagSubcategory('Carucioare ')" href = "#produse">Carucioare </a>
                            <a onclick="getEvomagSubcategory('Scaune Auto Copii si Inaltatoare ')" href = "#produse">Scaune Auto Copii si Inaltatoare </a>
                            <a onclick="getEvomagSubcategory('Accesorii transport ')" href = "#produse">Accesorii transport </a>
                            <a onclick="getEvomagSubcategory('Biberoane si tetine ')" href = "#produse">Biberoane si tetine </a>
                            <a onclick="getEvomagSubcategory('Suzete ')" href = "#produse">Suzete </a>
                            <a onclick="getEvomagSubcategory('Incalzitoare biberoane si hrana ')" href = "#produse">Incalzitoare biberoane si hrana </a>
                            <a onclick="getEvomagSubcategory('Babyphone ')" href = "#produse">Babyphone </a>
                            <a onclick="getEvomagSubcategory('Monitoare video bebelusi ')" href = "#produse">Monitoare video bebelusi </a>
                            <a onclick="getEvomagSubcategory('Lampi de veghe ')" href = "#produse">Lampi de veghe </a>
                            <a onclick="getEvomagSubcategory('Cadite bebelusi ')" href = "#produse">Cadite bebelusi </a>
                            <a onclick="getEvomagSubcategory('Olite ')" href = "#produse">Olite </a>
                        </div> </div>
                    <div class ="dropdownSecond">
                        <a onclick="getEvomagCategory('Casa, Decoratiuni %26amp; Bricolaj')" class = "dropbtnSecond" href="#produse"> Casa, Decoratiuni &amp; Bricolaj </a>
                        <div class = "dropdown-content-second">
                            <a onclick="getEvomagSubcategory('Masini de tuns iarba ')" href = "#produse">Masini de tuns iarba </a>
                            <a onclick="getEvomagSubcategory('Motosape ')" href = "#produse">Motosape </a>
                            <a onclick="getEvomagSubcategory('Motocultoare ')" href = "#produse">Motocultoare </a>
                            <a onclick="getEvomagSubcategory('Becuri cu LED ')" href = "#produse">Becuri cu LED </a>
                            <a onclick="getEvomagSubcategory('Iluminare exterioara ')" href = "#produse">Iluminare exterioara </a>
                            <a onclick="getEvomagSubcategory('Corpuri de iluminat de interior ')" href = "#produse">Corpuri de iluminat de interior </a>
                            <a onclick="getEvomagSubcategory('Aparate de sudura si invertoare profesionale ')" href = "#produse">Aparate de sudura si invertoare profesionale </a>
                            <a onclick="getEvomagSubcategory('Accesorii aparate de sudura ')" href = "#produse">Accesorii aparate de sudura </a>
                            <a onclick="getEvomagSubcategory('Gratare gradina ')" href = "#produse">Gratare gradina </a>
                            <a onclick="getEvomagSubcategory('Unelte de taiat ')" href = "#produse">Unelte de taiat </a>
                            <a onclick="getEvomagSubcategory('Unelte pentru constructii ')" href = "#produse">Unelte pentru constructii </a>
                            <a onclick="getEvomagSubcategory('Unelte de dulgherit ')" href = "#produse">Unelte de dulgherit </a>
                        </div> </div>


                </div>
            </div>
            <div class="dropdown">
                <button onclick="getAmazonGoogle()" class="dropbtn">
                    <img id = "bigger" src = "Imagini/amazoogle.png">
                </button>
            </div>

            <script>
                function getAmazonGoogle() {
                    const Http = new XMLHttpRequest();
                    const url = "https://comittw.herokuapp.com/search_product_api?content_search=" + document.getElementById('searchBar').value;
                    Http.open("GET", url);
                    Http.send();
                    document.getElementById('searchBar').value = '';
                    Http.onreadystatechange= (e) => {
                        const result =JSON.parse(Http.responseText);
                        var out = "";
                        var i;
                        for(i = 0; i < result['amazon'].length; i++) {
                            out += '<div class = "produs"><a target = "_blank" href="' + result['amazon'][i].link_produs + '">' +
                                '<img class = "imagine_produs_api" src ="' + result['amazon'][i].imagine_produs + '"' +
                                ' alt = "imagine produs" > ' + '</a><span class = "nextToImageAmazon">' + result['amazon'][i].nume_produs +
                                '<br>' + result['amazon'][i].pret_produs + '<br>Rating: ' + result['amazon'][i].rating_produs + '<br>' + '</span></div><br>';
                        }
                        for(i = 0; i < result['google'].length; i++) {
                            out += '<div class = "produs"><a target = "_blank" href="' + result['google'][i].link_produs + '">' +
                                '<img class = "imagine_produs_api" src ="Imagini/amazoogle.png"' +
                                ' alt = "imagine produs_api" > ' + '</a><span class = "nextToImageGoogle">' + result['google'][i].nume_produs +
                                '<br>' + result['google'][i].pret_produs + '<br>Rating: ' + result['google'][i].rating_produs + '<br>' + '</span></div><br>';
                        }

                        document.getElementById("produse").innerHTML = out;
                        window.location.hash = '#produse';
                    };
                }

                function convert(arr) {
                    let x = JSON.parse(arr);
                    for(var i = x.length - 1; i >= 0; i--) {
                        if(x[i] != null) {
                            return x[i][1];
                        }
                    }
                    return null;
                }

            </script>

            <a href = "#about">Despre</a>

            <li class = "noDecoration" ><a class="active" href = "#login" id = "auth"> <?php auth();?> </a></li>
        </div>

        <script>
            window.location.hash = '#about';
        </script>

		<div class = "target">

			<div id = "login">
				<form action="" method = "post">
					<a class = "right" href = "#createAccount">Creeaza cont!</a>
					<img id = "login-replacement" src = "./Imagini/login_transparent.png" alt = "login">
					<div class = "login-container">
						<label for = "uname"><b>Username</b></label>
						<input type = "text" placeholder="Introduceti numele de utilizator" name = "uname" id = "uname"><br>

						<label for = "psw"><b>Password</b></label>
						<input type = "password" placeholder="Introduceti parola" name = "psw" id = "psw"><br>

						<button type = "submit" id = "auth2"> <?php auth(); ?> </button><br><br>


						<label>
							<input type="checkbox" checked = "checked" name="remember"> Tine-ma minte
						</label>
					</div>
					<div>
						<button type = "button" class = "cancelbtn"> Anuleaza </button>
						<div><a class = "right" href = "#forgotPassword" > Ati uitat parola?</a></div><br>
					</div>
				</form>
					<div class = "center">
						<?php
							login(1);
						?>

				</div>
			</div>

			<div id = "about">
				<h3>ComIt (Compare It!)</h3>
				<p class = "center">
				Pe baza unui API REST ori GraphQL propriu, realizati o aplicatie Web – disponibila, de asemenea, ca extensie de navigator Web – care furnizeaza utilizatorilor autentificati sau nu studii comparative privitoare la (fluctuatia de) preturi ori alte caracteristici – e.g., model mai recent, varianta similara etc. – asociate unor articole/servicii apartinand unei/unor categorii de interes (electrocasnice, incaltaminte sport, API-uri de recomandare etc.). Datele analizate vor fi preluate din surse multiple (fluxuri de stiri, API-uri disponibile, via scraping - minim 3) oferite de situri de profil ce vor putea fi precizate de utilizator. Recomandarile generate vor fi disponibile si sub forma de fluxuri de stiri RSS si partajate pe minim o retea sociala folosind hashtag-ul #comit.
				</p>
                <p class = "center">
                    <a target = "_blank" href = "ScholarlyHTML/ScholarlyHTML.html">Aici</a> se poate gasi documentatia.
                </p>
                <p class = "center">
                    <a target = "_blank" href = "Ghid%20de%20utilizare/GhidUtilizare.html">Aici</a> se poate gasi ghidul de utilizare.
                </p>
			</div>
			<div id = "createAccount">
				<form action="" method = "post">
					<img id = "create-replacement" src = "./Imagini/create_transparent.png" alt = "create">
					<div class = "login-container">
						<label for = "lname"><b>Numele</b></label>
						<input type = "text" placeholder="Numele..." name = "lname" id = "lname" required><br>

						<label for = "fname"><b>Prenume</b></label>
						<input type = "text" placeholder="Prenumele..." name = "fname" id = "fname" required><br>

						<label for = "email"><b>Email</b></label>
						<input type = "text" placeholder="Email-ul..." name = "email" id = "email"><br>

						<label for = "iuname"><b>Username</b></label>
						<input type = "text" placeholder="Username-ul..." name = "iuname" id = "iuname" required><br>

						<label for = "ipsw"><b>Parola</b></label>
						<input type = "password" placeholder="" name = "ipsw" id = "ipsw" required><br>

						<button type = "submit">Creare cont</button><br><br>

					</div>
					<div>
						<button type = "button" class = "cancelbtn"> Anuleaza </button>
						<div><a class = "right" href = "#login" > Aveti deja cont?</a></div><br>
					</div>
				</form>
				<div class ="center">
					<?php
						signIn();
					?>
				</div>
			</div>

            <script>
                function emagNews() {
                    const Http = new XMLHttpRequest();
                    const url = "https://comittw.herokuapp.com/news/emag";
                    Http.open("GET", url);
                    Http.send();
                    Http.onreadystatechange= (e) => {
                        document.getElementById('xml').innerHTML = '<h1 class = "center">Flux de stiri cu produsele la oferta</h1>' +  Http.responseText;
                        window.location.hash("#xml");
                    };
                }

                function evomagNews() {
                    const Http = new XMLHttpRequest();
                    const url = "https://comittw.herokuapp.com/news/evomag";
                    Http.open("GET", url);
                    Http.send();
                    Http.onreadystatechange= (e) => {
                        document.getElementById('xml').innerHTML = '<h1 class = "center">Flux de stiri cu produsele la oferta</h1>' + Http.responseText;
                        window.location.hash("#xml");
                    };
                }

                function getEmagCategory(parameter_id) {
                    const Http = new XMLHttpRequest();
                    const url = "https://comittw.herokuapp.com/get_products/emag?category_name=" + parameter_id;
                    Http.open("GET", url);
                    Http.send();
                    Http.onreadystatechange= (e) => {
                        const result = JSON.parse(Http.responseText);
                        parseResultCategory(result, parameter_id);
                    };
                }

                function getEvomagCategory(parameter_id) {
                    const Http = new XMLHttpRequest();
                    const url = "https://comittw.herokuapp.com/get_products/evomag?category_name=" + parameter_id;
                    Http.open("GET", url);
                    Http.send();

                    Http.onreadystatechange= (e) => {
                        const result = JSON.parse(Http.responseText);
                        parseResultCategory(result, parameter_id);
                    };
                }

                function getEmagSubcategory(parameter_id) {
                    const Http = new XMLHttpRequest();
                    const url = "https://comittw.herokuapp.com/get_products/subcategory/emag?subcategory_name=" + parameter_id;
                    Http.open("GET", url);
                    Http.send();

                    Http.onreadystatechange= (e) => {
                        const result = JSON.parse(Http.responseText);
                        parseResultCategory(result, parameter_id);
                    };
                }

                function getEvomagSubcategory(parameter_id) {
                    const Http = new XMLHttpRequest();
                    const url = "https://comittw.herokuapp.com/get_products/subcategory/evomag?subcategory_name=" + parameter_id;
                    Http.open("GET", url);
                    Http.send();

                    Http.onreadystatechange= (e) => {
                        const result = JSON.parse(Http.responseText);
                        parseResultCategory(result, parameter_id);
                    };
                }

                function convert(arr) {
                    let x = JSON.parse(arr);
                    for(var i = x.length - 1; i >= 0; i--) {
                        if(x[i] != null) {
                            return x[i][1];
                        }
                    }
                    return null;
                }
                function parseResultCategory(result) {
                    var out = "";
                    var i;
                    for(i = 0; i < result.length; i++) {
                        out += '<div class = "produs"><a target = "_blank" href="' + result[i].link_produs + '">' +
                            '<img class = "imagine_produs" src ="' + result[i].imagine_produs + '"' +
                            ' alt = "imagine produs" > ' + '</a><span class = "nextToImage">' + result[i].nume_produs +
                            '<br>' + 'Pret: ' + convert(result[i].pret_produs) + '<br>' +
                            'Rating: ' + result[i].rating_produs + '<br>' +
                            'Valabilitate: ' + result[i].valabilitate_produs + '<br>' + '</span></div><br>';
                    }
                    document.getElementById('produse').innerHTML = out;
                    window.location.hash = '#produse';
                }
            </script>
            <script>
                function run() {
                    let shown = 0;
                    const Http = new XMLHttpRequest();
                    let url = "";
                    if(document.getElementById('emagRadioButton').checked) {
                        url = "https://comittw.herokuapp.com/scrapper/run?name=emag";
                    }
                    else {
                        url = "https://comittw.herokuapp.com/scrapper/run?name=evomag";
                    }
                    Http.open("GET", url);
                    Http.send();

                    Http.onreadystatechange= (e) => {
                        if(shown === 0 && Http.responseText !== "") {
                            window.alert(Http.responseText);
                            shown = 1;
                        }
                    };
                }

                function stop() {
                    const Http = new XMLHttpRequest();
                    let url = "";
                    let shown = 0;
                    if(document.getElementById('emagRadioButton').checked) {
                        url = "https://comittw.herokuapp.com/scrapper/stop?name=emag";
                    }
                    else {
                        url = "https://comittw.herokuapp.com/scrapper/stop?name=evomag";
                    }
                    Http.open("GET", url);
                    Http.send();

                    Http.onreadystatechange= (e) => {
                        if(shown === 0 && Http.responseText !== "") {
                            window.alert(Http.responseText);
                            shown = 1;
                        }                    };
                }

                function statusButton() {
                    const Http = new XMLHttpRequest();
                    let url = "";
                    let shown = 0;
                    if(document.getElementById('emagRadioButton').checked) {
                        url = "https://comittw.herokuapp.com/scrapper/status?name=emag";
                    }
                    else {
                        url = "https://comittw.herokuapp.com/scrapper/status?name=evomag";
                    }                    Http.open("GET", url);
                    Http.send();

                    Http.onreadystatechange= (e) => {
                        if(shown === 0 && Http.responseText !== "") {
                            window.alert(Http.responseText);
                            shown = 1;
                        }
                    };
                }

                function send() {
                    const Http = new XMLHttpRequest();
                    let shown = 0;
                    const url = "https://comittw.herokuapp.com/send/message?message=" + document.getElementById('message').value +  "#comit";
                    document.getElementById('message').value = "";
                    Http.open("GET", url);
                    Http.send();

                    Http.onreadystatechange= (e) => {
                        if(shown === 0 && Http.responseText !== "") {
                            window.alert(Http.responseText);
                            shown = 1;
                        }                    };
                }

                function activate() {
                    const Http = new XMLHttpRequest();
                    let url = "";
                    let shown = 0;
                    if(document.getElementById('emagRadioButton').checked) {
                        url = "https://comittw.herokuapp.com/scrapper/activate?name=emag";
                    }
                    else {
                        url = "https://comittw.herokuapp.com/scrapper/activate?name=evomag";
                    }                    Http.open("GET", url);
                    Http.send();

                    Http.onreadystatechange= (e) => {
                        if(shown === 0 && Http.responseText !== "") {
                            window.alert(Http.responseText);
                            shown = 1;
                        }
                    };
                }

                function deactivate() {
                    const Http = new XMLHttpRequest();
                    let url = "";
                    let shown = 0;
                    if(document.getElementById('emagRadioButton').checked) {
                        url = "https://comittw.herokuapp.com/scrapper/deactivate?name=emag";
                    }
                    else {
                        url = "https://comittw.herokuapp.com/scrapper/deactivate?name=evomag";
                    }                    Http.open("GET", url);
                    Http.send();

                    Http.onreadystatechange= (e) => {
                        if(shown === 0 && Http.responseText !== "") {
                            window.alert(Http.responseText);
                            shown = 1;
                        }
                    };
                }

            </script>
            <div id = "admin">
                <div class = "center">
                    <form>
                        <input type = "radio" id ="emagRadioButton" name = "scrapper" value ="emag" checked = "checked"><label for = "emagRadioButotn">Emag</label>
                        <input type = "radio" id = "evomagRadioButton" name = "scrapper" value = "evomag"><label for = "evomagRadioButton">Evomag</label>
                    </form>
                    <input type = "text" id = "message" name ="message" placeholder="Mesaj pentru facebook"><br>
                    <button onclick="activate()" class= "adminButtons">Activate</button>
                    <button onclick="deactivate()" class= "adminButtons">Deactivate</button>
                    <button onclick="run()" class= "adminButtons">Run</button>
                    <button onclick="stop()" class= "adminButtons">Stop</button>
                    <button onclick="statusButton()" class= "adminButtons">Status</button>
                    <button onclick="send()" class= "adminButtons">Send</button>
                </div>
            </div>

            <div id = "searchTarget">

            </div>

            <div id = "produse">

            </div>


            <div id = "xml">

            </div>

		</div>

		<div class = "copyright">
			<span>Copyright &copy 2020 Cernovschi Ioan - Valentin & Cojocariu Magda</span>
		</div>
	</body>
</html>
