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
#Thanks to: http://www.sitepoint.com/uploading-files-cgi-perl/

#use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use URI::Escape;
#print "Content-type: text/html\n\n";

$CGI::POST_MAX = 1024 * 5000;
my $safe_filename_characters = "a-zA-Z0-9_.-";
my $upload_dir = '/tmp';

my $query = new CGI;
my $filename = $query->param("photo");

if ( !$filename )
{
	print "Content-Type: text/html\n";
	print "Status: 302 Moved\n";
	print "Location: /~dwilches/sbi/cgi-bin/formulary.pl?error=NoFile\n";
	print "\n";
	exit;
}

my ( $name, $path, $extension ) = fileparse ( $filename, '\..*' ); $filename = $name . $extension;
$filename =~ tr/ /_/; $filename =~ s/[^$safe_filename_characters]//g;

if ( $filename =~ /^([$safe_filename_characters]+)$/ )
{
	$filename = $1;
}
else
{
	die "Filename contains invalid characters";
}

my $upload_filehandle = $query->upload("photo");

open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "Error creando archivo: $upload_dir/$filename";
binmode UPLOADFILE;
while ( <$upload_filehandle> )
{
	print UPLOADFILE;
}
close UPLOADFILE;

# Ejecución del script de AConde:
print "Content-Type: text/html\n";
print "Status: 302 Moved\n";
print "Location: /~dwilches/sbi/cgi-bin/SBI.pl?imagetype=UPLOAD&imagename=" . uri_escape("$filename") . "\n";
print "\n";
