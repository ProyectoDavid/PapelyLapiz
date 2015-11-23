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

my $GENERATED_DIR = '/home/dwilches/pyl/ImageProcessing/Execution/Log';


# Eliminar imágenes generadas por sesiones anteriores:
chdir($GENERATED_DIR) or die("El directorio $GENERATED_DIR no existe\n");
opendir(GENERATED_DIR, $GENERATED_DIR);
while (readdir(GENERATED_DIR))
{
	unlink if (/\.png$/ || /\.tif$/ || /\.txt$/);
}
closedir(GENERATED_DIR);


print << "EOF";

<HTML>
	<HEADER>
		<base href="/~dwilches/sbi/" />
		<META http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE" />
		<META HTTP-EQUIV="Pragma" CONTENT="no-cache" />
		<META HTTP-EQUIV="Expires" CONTENT="0" />
		<LINK rel="STYLESHEET" href="css/style.css" type="text/css">
		<TITLE>SBI for animation generation</TITLE>
	</HEADER>
	<BODY>
		<H1>Resultados de la ejecuci&oacute;n</H1>
		<P>Se est&aacute; ejecutando el programa de detecci&oacute;n de patrones.
		Espere un momento por favor mientras se procesa esta imagen.</P>
		<P>Una vez el proceso termine de click aqui para generar la imagen: <A HREF='cgi-bin/VideoGenerator.pl?render_low_quality=True&render_video=False' target="output">Generar imagen</A> o aqui para generar el video: <A HREF='cgi-bin/VideoGenerator.pl?render_low_quality=True&render_video=True' target="output">Generar video</A></P>
		
		<TABLE WIDTH="100%" BORDER="0">
		<TR>
			<TD width='200px'>
				<h2>Resultados</h2>
				<iframe width='200px' height='450px' class='scrollableArea'
					src='cgi-bin/MostrarResultados.pl?imagename=$imagename&imagetype=$imagetype'>
				</iframe>
			</TD>
			<TD>
				<h2>Imagen procesada</h2>
				<iframe width='100%' height='450px' class='scrollableArea' id='imageiframe' name='imageiframe'
					src='cgi-bin/MostrarImagen.pl?imagename=$imagename'>
				</iframe>
			</TD>
		</TR>
		<TR>
			<TD COLSPAN='2'>
			<A HREF="/~dwilches/sbi/">Volver al inicio</A>
			<p class="footer">Creado por:<br/>Daniel Wilches, Agust&iacute;n Conde.</p>
			</TD>
		</TABLE>
	</BODY>
</HTML>
EOF
