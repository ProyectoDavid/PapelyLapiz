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
my $render_low_quality = $query->param("render_low_quality");
my $render_video = $query->param("render_video");

print << "EOF";

<HTML>
	<HEADER>
		<META http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<base href="/~dwilches/sbi/" />
		<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE" />
		<META HTTP-EQUIV="Pragma" CONTENT="no-cache" />
		<META HTTP-EQUIV="Expires" CONTENT="0" />
		<LINK rel="STYLESHEET" href="css/style.css" type="text/css">
	</HEADER>
	<BODY>
EOF

$out = `RENDER_VIDEO=$render_video RENDER_LOW_QUALITY=$render_low_quality /opt/blender/blender -P /home/dwilches/pyl/VideoGenerator/VideoGenerator.py -b /home/dwilches/pyl/VideoGenerator/empty_scene.blend 2>&1 >> /home/dwilches/public_html/sbi/output/VideoGenerator.log`;


if ($render_video eq 'True')
{
	print "<EMBED SRC='output/video0001-0300.ogg' width='640' height='480'></EMBED>";
}
else
{
	print "<IMG SRC='output/imagen.png' />"
}

print << "EOF";
	</BODY>
</HTML>
EOF

