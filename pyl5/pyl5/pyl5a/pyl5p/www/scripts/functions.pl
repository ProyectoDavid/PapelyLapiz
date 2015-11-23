#
#Papel y Lapiz - Software para la creacion de pequeños cortos.
#Copyright (C) 2015  Universidad de Los Andes - Proyecto DAVID.   
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation,
#Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#!/usr/bin/perl

use XML::DOM;
use XML::XPath;

require 'paths.pl';

$FILES_PER_ROW = 3;
@actors = ();
@noises = ();
@text = ();
@sounds = ();
my $radio = '';

sub GetVocabularyFilename()
{
	$IMAGE_PROCESSING_BASE . '/Execution/vocabulary.xml';
}

sub ExecuteImageProcessing
{
	unlink("$WEB_ROOT_PATH/output/images/$SCENE_DESCRIPTION_FILE");
	unlink("$WEB_ROOT_PATH/output/images/$IMAGE_PROCESSING_LOG");
	print `./ImageProcessing.sh '$_[0]' '$WEB_ROOT_PATH/output/images/$_[1]' '$SCENE_DESCRIPTION_FILE' '$IMAGE_PROCESSING_LOG' '$ROOT_PATH/ImageProcessing/bin'`;
}

sub ExecuteVideoGenerator
{
	unlink($VIDEO_GENERATOR_LOG);
	if ($_[1] eq 'False')
	{
		`rm $WEB_ROOT_PATH/output/images/$_[2]/output.png`;
	}
	else
	{
		`rm $WEB_ROOT_PATH/output/images/$_[2]/output.ogg`;
	}
	print `./VideoGenerator.sh $_[0] $_[1] '$WEB_ROOT_PATH/output/images/$_[2]' '$VIDEO_GENERATOR_OUTPUT' '$SCENE_DESCRIPTION_FILE' '$VIDEO_GENERATOR_LOG' '$ROOT_PATH' '$WEB_ROOT_PATH/output/images/$_[2]/$SCORE_DESCRIPTION_FILE'`;
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
	
	# Agregar lista de sonidos
	push @sounds, 'Default';
	push @sounds, 'Pajaro';
	push @sounds, 'Ardilla';
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

			# Opciones sonidos	
			print "<div>";
			$checked = 'checked';
			foreach $sound (@sounds)
			{
				print "<input type='radio' name='sound$actor->{Image}' value='$sound' $checked/>$sound<br/>";
				if ($checked eq 'checked') {
					$checked = '';
				}
			}
			$radio = $radio."sound$actor->{Image}\n";
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


	print "<button type='button'>Agregar sonidos</button>";
	$radio = 'yukiho';
	`./writeMini.sh '$radio' '/var/www/pyl3/www/cgi-bin/idol.xml'`;
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
		if ($actor->{Type} eq 'Text')
		{
			print "<P>$actor->{Text}<BR/>";
			
			# Opciones imagen correcta			
			print "<div>";
			print "<input type='radio' name='group$actor->{Text}' value='OK' onclick='escribir(\"testin\");' checked />OK";
			print "<input type='radio' name='group$actor->{Text}' value='KO' onclick='escribir(\"KO\");'/> KO<BR/>";
			
			print "</div>";
			print "<button type='button' onclick='alert(\"test\");'>OK?</button>";

			# Opciones sonidos	
			print "<div>";
			$checked = 'checked';
			foreach $sound (@sounds)
			{
				print "<input type='radio' name='sound$actor->{Text}' value='$sound' $checked/>$sound<br/>";
				if ($checked eq 'checked') {
					$checked = '';
				}
			}
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

	print "<button type='button'>Agregar sonidos</button>";
	
	my $vocab = '<i><idol name="haruka"/></i>';
	#`./writeMini.sh '$vocab' '/var/www/pyl3/www/cgi-bin/idol.xml'`;
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

sub PrintSymbolSet()
{
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

		my $node = $nodes->item ($i);
		my $href = $node->getAttribute ("shape");
		my $name = $node->getAttribute ("asset");
		print "<TD><IMG SRC='output/$href' /><BR/><B>Asset:</B> $name</TD>";

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
	print `./SoundFilm.sh '$IMAGE_PROCESSING_BASE/Execution/vocabularyjm.moreno743.xml' '$WEB_ROOT_PATH/output/images/$_[0]/script.xml' '$WEB_ROOT_PATH/output/images/$_[0]/score.xml' '$IMAGE_PROCESSING_BASE' '$WEB_ROOT_PATH/output/images/$_[0]/SoundFilm.log'`;
}

return 1;

