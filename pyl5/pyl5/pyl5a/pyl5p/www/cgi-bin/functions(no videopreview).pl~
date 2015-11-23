
#!/usr/bin/perl

use XML::DOM;
use XML::XPath;

require 'paths.pl';

$FILES_PER_ROW = 3;
@actors = ();
@noises = ();
@text = ();
@soundsActors = ();
$radioActors = '';
@soundsAnimations = ();
$radioAnimations = '';

sub GetVocabularyFilename()
{
	$IMAGE_PROCESSING_BASE . '/Execution/vocabulary.xml';
}

sub ExecuteImageProcessing
{
	unlink("$WEB_ROOT_PATH/output/images/$_[1]/$SCENE_DESCRIPTION_FILE");
	unlink("$WEB_ROOT_PATH/output/images/$_[1]/$IMAGE_PROCESSING_LOG");
	unlink("$WEB_ROOT_PATH/output/images/$_[1]/output.png");
	
	print `./ImageProcessing.sh '$_[0]' '$WEB_ROOT_PATH/output/images/$_[1]' '$SCENE_DESCRIPTION_FILE' '$IMAGE_PROCESSING_LOG' '$ROOT_PATH/ImageProcessing/bin'`;
}

sub ExecuteVideoGenerator
{
	#unlink($VIDEO_GENERATOR_LOG);
	#if ($_[1] eq 'False')
	#{
	#	`rm $WEB_ROOT_PATH/output/images/$_[2]/output.png`;
	#	print `$ROOT_PATH/www/cgi-bin/VideoGenerator.sh $_[0] $_[1] '$WEB_ROOT_PATH/output/images/$_[2]' '$VIDEO_GENERATOR_OUTPUT' '$SCENE_DESCRIPTION_FILE' '$VIDEO_GENERATOR_LOG' '$ROOT_PATH' '$ROOT_PATH/ImageProcessing/Execution/score.xml'`;

	#}
	#else
	#{
	#	`rm $WEB_ROOT_PATH/output/images/$_[2]/output.ogg`;
		
	#	print `./VideoGenerator.sh $_[0] $_[1] '$WEB_ROOT_PATH/output/images/$_[2]' '$VIDEO_GENERATOR_OUTPUT' '$SCENE_DESCRIPTION_FILE' '$VIDEO_GENERATOR_LOG' '$ROOT_PATH' '$WEB_ROOT_PATH/output/images/$_[2]/$SCORE_DESCRIPTION_FILE'`;
		
	#	`$ROOT_PATH/ImageProcessing/SoundFilm/ffmpeg -i $WEB_ROOT_PATH/output/images/$_[2]/output.mpg -vf "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf: text='$_[7]': r=50: \ x=(w-tw)/2: y=h-(2*lh): fontcolor=black: box=0.5: boxcolor=#50FFFFFF" -y $WEB_ROOT_PATH/output/images/$_[2]/outputcard.mpg`;

	#	open FILE, ">$WEB_ROOT_PATH/output/images/$_[2]/mail.properties" or die $!;
	#	print FILE "from=$_[3]\n";
	#	print FILE "mailto=$_[6]\n";
	#	print FILE "subject=$_[7]\n";
	#	print FILE "attachment=$WEB_ROOT_PATH/output/images/$_[2]/outputcard.mpg\n";
	#	print FILE "html=$_[8]";
	#	close FILE;
		
		#Se que no es la mejor forma de hacerlo pero es mejor que reiniciar.
	#	`/usr/lib/jvm/java-7-openjdk/bin/java -jar $ROOT_PATH/EMailGenerator/PYLMail.jar "$WEB_ROOT_PATH/output/images/$_[2]/mail.properties" "$ROOT_PATH/EMailGenerator/mailsender.properties"`;
	#}
}

sub GetImageProcessingLog
{
	($foldername) = @_;

	my $BLOCK_DELIM = '';

	$components = {};

	open LOG_FILE, "$WEB_ROOT_PATH/output/images/$foldername/$IMAGE_PROCESSING_LOG";

	while(<LOG_FILE>)
	{
		chomp;

		# Las líneas en blanco me indican que debo poner una imagen en el HTML (posiblemente).
		# Si no es una línea en blanco, tratar de entenderla
		if ($_ ne $BLOCK_DELIM)
		{
			# Solo me interesan estos componentes:
			next unless /^# (\w*): (.*)$/;

			$components->{$1} = $2;

			if ($1 eq 'Bounds')
			{
				if ($2 =~ /\(([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)\)/)
				{
					$components->{X} = $1;
					$components->{Y} = $2;
					$components->{W} = $3;
					$components->{H} = $4;
				}
			}

			next;
		}

		# Si llega aqui es una linea en blanco
		push @actors, $components if $components->{Type} eq 'Actor';
		push @actors, $components if $components->{Type} eq 'Arrow';
		push @noises, $components if $components->{Type} eq 'Noise';
		push @text, $components if $components->{Type} eq 'Text';
		push @noises, $components if $components->{Type} eq 'NotRecognized';

		$components = {};
	}

	# Agregar lista de sonidos de actores
	push @soundsActors, 'Default';
	push @soundsActors, 'Pajaro No. 1';
	push @soundsActors, 'Pajaro No. 2';
	push @soundsActors, 'Pajaro No. 3';
	push @soundsActors, 'Ardilla';
	
	# Agregar lista de sonidos de animaciones
	push @soundsAnimations, 'Default';
	push @soundsAnimations, 'JUMP No. 1';
	push @soundsAnimations, 'JUMP No. 2';
	push @soundsAnimations, 'JUMP No. 3';
	push @soundsAnimations, 'WALK';
}

sub PrintActors
{

print("
	<script type='text/javascript'>
	function escribir(text) {

    /*var sw : StreamWriter = new StreamWriter(\"testin.txt\");

    sw.WriteLine(text);

    sw.Flush();

    sw.Close();*/alert(text);
	}
</script>");
        
	($foldername) = @_;

	my $file_number = 0;
	print "<TABLE width='100%' align='center' border='0'>\n";
	foreach $actor (@actors)
	{
		# Just pretty ... :
		#{
		if (($file_number % $FILES_PER_ROW) == 0)
		{
			print "<TR>\n";
		}
		#}

		# The real thing:
		print " <TD valign='top'>".
			"<A onClick='mostrarRecuadro($actor->{X},$actor->{Y},$actor->{W},$actor->{H})' ".
			"onMouseOver=\"cambiarCursor('pointer')\" onMouseOut=\"cambiarCursor('default')\">";
		if ($actor->{Type} eq 'Actor')
		{
			print "<IMG SRC='output/images/$foldername/Log/Actors/$actor->{Image}' BORDER='1' WIDTH='50'/><BR/>";
			
			# Opciones imagen correcta			
			print "<div>";
			print "<input type='radio' name='group$actor->{Image}' value='OK' onclick='escribir(\"testin\");' checked />OK";
			print "<input type='radio' name='group$actor->{Image}' value='KO' onclick='escribir(\"KO\");'/> KO<BR/>";
			
			print "</div>";
			print "<button type='button' onclick='alert(\"test\");'>OK?</button>";

			# We print sound options
			print "<div>";
			$checked = 'checked';
			$anElement = '';
			foreach $sound (@soundsActors)
			{
			
				if ( 	( $sound =~ m/Default/) ||
						( $sound =~ m/Pajaro/ && $actor->{Image} =~ m/Pajaro/) ||
						( $sound =~ m/Ardilla/ && $actor->{Image} =~ m/Ardilla/)  ) {
				
					print "<input type='radio' name='sound$actor->{Image}' value='$sound' $checked/>$sound<br/>";
					if ($checked eq 'checked') {
						$checked = '';
					}
				}
			}
			$radioActors = $radioActors."sound$actor->{Image}\n";
			print "</div>";
		}
		else
		{
			print "<IMG SRC='output/images/$foldername/Log/Arrows/$actor->{Image}' BORDER='1' WIDTH='50'/><BR/>";
		}
		print "</A></TD><TD>";

		print "<b>Object:</b><br/>$actor->{Type}<br/>"
			if $actor->{'Type'} ne 'Actor';
		print "<b>Object:</b><br/>$actor->{Asset}<br/>"
			if $actor->{'Type'} eq 'Actor';

		print "<b>Animation:</b><br/>$actor->{Animation}<br/>"
			if $actor->{'Animation'} ne '';

		print "<BR/></TD>\n";

		# Just pretty ... :
		#{
		$file_number++;
		if (($file_number % $FILES_PER_ROW) == 0)
		{
			print "</TR>\n";
		}
		#}
	}

	print "</TABLE>";

	`./writeMini.sh '$radioActors' '/var/www/pyl3/www/cgi-bin/soundsActors.txt'`;
	
	return
}

sub PrintText
{
print("
	<script type='text/javascript'>
	function escribir(text) {

    /*var sw : StreamWriter = new StreamWriter(\"testin.txt\");

    sw.WriteLine(text);

    sw.Flush();

    sw.Close();*/alert(text);
	}
</script>");
	($foldername) = @_;

	my $file_number = 0;
	print "<TABLE width='100%' align='center' border='0'>\n";
	foreach $actor (@text)
	{
		# Just pretty ... :
		#{
		if (($file_number % $FILES_PER_ROW) == 0)
		{
			print "<TR>\n";
		}
		#}

		# The real thing:
		print " <TD valign='top'>".
			"<A onMouseOver=\"cambiarCursor('pointer')\" onMouseOut=\"cambiarCursor('default')\">";
		@radio = '';
		if ($actor->{Type} eq 'Text')
		{
			print "<P>$actor->{Text}<BR/>";
			
			# Opciones imagen correcta			
			print "<div>";
			print "<input type='radio' name='group$actor->{Text}' value='OK' onclick='escribir(\"testin\");' checked />OK";
			print "<input type='radio' name='group$actor->{Text}' value='KO' onclick='escribir(\"KO\");'/> KO<BR/>";
			
			print "</div>";
			print "<button type='button' onclick='alert(\"test\");'>OK?</button>";

			# We print sound options
			print "<div>";
			$checked = 'checked';
			foreach $sound (@soundsAnimations)
			{
			
				if ( 	( $sound =~ m/Default/) ||
						( $sound =~ m/JUMP/ && $actor->{Text} =~ m/JUMP/) ||
						( $sound =~ m/WALK/ && $actor->{Text} =~ m/WALK/)  ) {
						
					print "<input type='radio' name='soundword$actor->{Text}' value='$sound' $checked/>$sound<br/>";
					if ($checked eq 'checked') {
						$checked = '';
					}
				}
			}
			$radioAnimations = $radioAnimations."soundword$actor->{Text}\n";
			print "</div>";
		}
		print "</A></TD><TD>";

		print "<BR/></TD>\n";

		# Just pretty ... :
		#{
		$file_number++;
		if (($file_number % $FILES_PER_ROW) == 0)
		{
			print "</TR>\n";
		}
		#}
	}

	print "</TABLE>";

	`./writeMini.sh '$radioAnimations' '/var/www/pyl3/www/cgi-bin/soundsAnimations.txt'`;
}

sub PrintNoise()
{
	($foldername) = @_;

	my $file_number = 0;
	print "<TABLE width='100%' align='center'>\n";
	foreach $noise (@noises)
	{
		# Just pretty ... :
		#{
		if (($file_number % $FILES_PER_ROW) == 0)
		{
			print "<TR>\n";
		}
		#}

		# The real thing:
		print " <TD valign='top'>".
			"<A onClick='mostrarRecuadro($noise->{X},$noise->{Y},$noise->{W},$noise->{H})' ".
			"onMouseOver=\"cambiarCursor('pointer')\" onMouseOut=\"cambiarCursor('default')\">";
		if ($noise->{Type} eq 'Noise')
		{
			print "<IMG SRC='output/images/$foldername/Log/Noise/$noise->{Image}' BORDER=1>";
			print "</A><BR/>";
			print "Considered noise</BR>";
		}
		else
		{
			print "<IMG SRC='output/images/$foldername/Log/NotRecognized/$noise->{Image}' BORDER=1>";
			print "</A><BR/>";
			print "Unidentified object</BR>";
		}

		print "<BR/></TD>\n";

		# Just pretty ... :
		#{
		$file_number++;
		if (($file_number % $FILES_PER_ROW) == 0)
		{
			print "</TR>\n";
		}
		#}
	}
	print "</TABLE>";
}

sub PrintSymbolSet
{
	($lang) = @_;

	my $vocabulary_filename = GetVocabularyFilename();

	my $parser = new XML::DOM::Parser;
	my $doc = $parser->parsefile ($vocabulary_filename);

	my $nodes = $doc->getElementsByTagName ("object");
	my $n = $nodes->getLength;

	my $file_number = 0;
	print "<TABLE WIDTH='100%' align='center' border='0'>";
	for (my $i = 0; $i < $n; $i++)
	{
		# Just pretty ... :
		#{
		if (($file_number % $FILES_PER_ROW) == 0)
		{
			print "<TR>\n";
		}
		#}
		#my $lang = "es";
		my $node = $nodes->item ($i);
		my $href = $node->getAttribute ("shape");
		my $name = $node->getAttribute ($lang);
		print "<TD align='center'><IMG SRC='output/$href' /><BR/><B>$name</B></TD>";

		# Just pretty ... :
		#{
		$file_number++;
		if (($file_number % $FILES_PER_ROW) == 0)
		{
			print "</TR>\n";
		}
		#}
	}
	print "</TABLE>";

}

sub ExecuteSoundFilm
{
	unlink("$WEB_ROOT_PATH/output/images/$SCENE_DESCRIPTION_FILE");
	print `/var/www/pyl3/www/cgi-bin/SoundFilm.sh '/var/www/pyl3/ImageProcessing/Execution/vocabularyjm.moreno743.xml' '$WEB_ROOT_PATH/output/images/$_[0]/script.xml' '$WEB_ROOT_PATH/output/images/$_[0]/score.xml' '$IMAGE_PROCESSING_BASE' '$WEB_ROOT_PATH/output/images/$_[0]/SoundFilm.log' 'Default*Default*Default*Default*Default*Default*Default*Default*Default*Default*' 'Default*Default*Default*Default*Default*Default*Default*Default*Default*Default*'`;
}

sub GetRadioActors
{
	($foldername) = @_;

	my $BLOCK_DELIM = '';

	$components = {};
	my $myRadioActors = '';
	open ACTORS_FILE, "/var/www/pyl3/www/cgi-bin/soundsActors.txt";
	
	while(<ACTORS_FILE>)
	{
		chomp;
		$myRadioActors = $myRadioActors.$_.'#';
	}
	return $myRadioActors;
}

sub GetRadioAnimations
{
	($foldername) = @_;

	my $BLOCK_DELIM = '';

	$components = {};
	my $myRadioAnimations = '';
	open ANIMATIONS_FILE, "/var/www/pyl3/www/cgi-bin/soundsAnimations.txt";

	while(<ANIMATIONS_FILE>)
	{
		chomp;
		$myRadioAnimations = $myRadioAnimations.$_.'#';
	}
	return $myRadioAnimations;
}


return 1;

