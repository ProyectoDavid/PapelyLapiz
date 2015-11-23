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

#use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use Data::Dumper;
use File::Copy;

print "Content-type: text/html\n\n";

$| = 1;

my $query = new CGI;
my $imagetype = $query->param("imagetype");
my $imagename = $query->param("imagename");

my $THESIS_DIR = '/home/dwilches/pyl/ImageProcessing';
my $GENERATED_DIR = '/home/dwilches/pyl/ImageProcessing/Execution/Log';
my $IMAGE_TEST = '/home/dwilches/public_html/sbi/images/prueba';
my $UPLOAD_DIR = '/tmp';


# Eliminar imágenes generadas por sesiones anteriores:
chdir($GENERATED_DIR) or die("El directorio $GENERATED_DIR no existe\n");
opendir(GENERATED_DIR, $GENERATED_DIR);
while (readdir(GENERATED_DIR))
{
	unlink if (/\.png$/ || /\.tif$/ || /\.txt$/);
}
closedir(GENERATED_DIR);

if ($imagetype eq 'TEST')
{
	copy "$IMAGE_TEST/$imagename", "$GENERATED_DIR/Processing_$imagename";
}
else
{
	copy "$UPLOAD_DIR/$imagename", "$GENERATED_DIR/Processing_$imagename";
}

my $image  = "$GENERATED_DIR/Processing_$imagename";


chdir($THESIS_DIR) or die("El directorio $THESIS_DIR no existe\n");
print << "EOF";

<HTML>
	<HEADER>
		<META http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<base href="/~dwilches/sbi/" />
		<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE" />
		<META HTTP-EQUIV="Pragma" CONTENT="no-cache" />
		<META HTTP-EQUIV="Expires" CONTENT="0" />
		<LINK rel="STYLESHEET" href="css/style.css" type="text/css">
		<script type="text/javascript">
			function mostrarRecuadro(top,left)
			{
				var iframeDoc = window.parent.frames.imageiframe.document;
				var imagenRecuadro = iframeDoc.recuadro;
				
				imagenRecuadro.height = 50;
				imagenRecuadro.width = 50;
				
				var escala = iframeDoc.oculta.height / iframeDoc.imagen.height;
				
				imagenRecuadro.style.top = top / escala;
				imagenRecuadro.style.left = left / escala;
			}
			
			function cambiarCursor(nuevoCursor)
			{
				document.body.style.cursor = nuevoCursor;
			}
		</script>
	</HEADER>
	<BODY>
EOF

#print `/home/dwilches/public_html/sbi/cgi-bin/SBI-exec.sh '$image' /home/dwilches/public_html/sbi/output/ImageProcessing.log`;

# Mostrar imágenes generadas:

my $file_number = 0;
my $FILES_PER_ROW = 1;
my @actors = ();
my @noises = ();
my $BLOCK_DELIM = '';

print "<pre>";

$components = {};

open LOG_FILE, "/home/dwilches/public_html/sbi/output/ImageProcessing.log";
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
		
		if ($1 eq 'Center')
		{
			if ($2 =~ /\[(\d+)[^,]*, ([\d]+)[.\d]*\]/)
			{
				#$components{'Y'} = $1 - 25;
				#$components{'X'} = $2 - 25;
			}
		}
		
		next;
	}

	# Si llega aqui es una linea en blanco
	push @actors, $components if $components->{Type} eq 'Actor';
	push @noises, $components if $components->{'Type'} eq 'Noise';

	$components = {};
}

print "<h3>Objetos reconocidos</h3>";
print "<TABLE align='center'>\n";
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
	print "	<TD valign='top'>".
		"<A onClick='mostrarRecuadro($actors->{X},$actors->{Y})' onMouseOver=\"cambiarCursor('pointer')\" onMouseOut=\"cambiarCursor('default')\">".
		"<IMG SRC='output/images/Recognized/$actor->{Image}' BORDER='1' WIDTH='50'/><BR/>$actor->{Image}".
		"</A></TD></TR>".
		"<TR><TD>";
	
	print '<b>Objeto:</b><br/>' if $actor->{'Asset'} =~ s/\.mesh//;
	print $actor->{'Asset'} . '<br/>';
	
	print "<b>Animaci&oacute;n:</b><br/>$actor->{'Animation'}<br/>"
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


print "<h3>Objetos no reconocidos</h3>";
print "<TABLE align='center'>\n";
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
                "<A onClick='mostrarRecuadro($noise->{X},$noise->{Y})' onMouseOver=\"cambiarCursor('pointer')\" onMouseOut=\"cambiarCursor('default')\">".
                "<IMG SRC='output/images/Noise/$noise->{Image}' BORDER=1>".
                "</A><BR/>";

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

