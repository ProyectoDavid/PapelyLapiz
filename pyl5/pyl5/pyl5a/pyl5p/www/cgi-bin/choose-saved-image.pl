#!/usr/bin/perl

#use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use URI::Escape;

my $query = new CGI;
my $error = $query->param("error");

require 'template.pl';

BeginPage("Those are the files that you or other users have already uploaded. You can select one of these files to process them again.");

BeginSection("Select an image", "select-image", "fullwidth_div");

# Mostrar imágenes de prueba:
print "<TABLE align='center' border='2'>\n";
opendir(IMAGE_DIR, "$WEB_ROOT_PATH/output/images");
my $file_number = 0;
my $FILES_PER_ROW = 3;
while (readdir(IMAGE_DIR))
{
	next unless length($_) == 32;

	$dirname = $_;
	$filename = `ls $WEB_ROOT_PATH/output/images/$dirname/Processing_*`;

	$filename =~ s#.*/Processing_(.*)$#\1#;

	if (($file_number % $FILES_PER_ROW) == 0)
	{
		print "<TR>\n";
	}
	print "	<TD align='center'><B>$filename</B><BR/><A HREF='output/images/$dirname/Processing_$filename'>" .
			"<IMG SRC='output/images/$dirname/Processing_$filename' WIDTH='200'><BR/>" .
			"<A HREF='cgi-bin/SBI.pl?imagename=Processing_$filename&uploaddir=$dirname'>Ejecutar</A>" .
		"</TD>\n";
	
	$file_number++;
	if (($file_number % $FILES_PER_ROW) == 0)
	{
		print "</TR>\n";
	}
}
closedir(IMAGE_DIR);
print "</TABLE>";

EndSection();

EndPage();

