
#!/usr/bin/perl

use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use Data::Dumper;
use File::Copy;

require 'template.pl';
require 'functions.pl';

$| = 1;

my $query = new CGI;
my $quality = $query->param("render_low_quality");
my $video = $query->param("render_video");
my $imagefolder = $query->param("imagefolder");
my $nombrede = $query->param("nombrede");
my $mailde = $query->param("mailde");
my $nombrepara = $query->param("nombrepara");
my $mailpara = $query->param("mailpara");
my $subject = $query->param("subject");
my $atext = $query->param("atext");

ExecuteVideoGenerator($quality, $video, $imagefolder, $nombrede, $mailde, $nombrepara, $mailpara, $subject, $atext);

if ($video eq 'True')
{
	print "
<video width='640' height='480' controls='controls'>
	<source src='output/images/$imagefolder/output.mpg' type='video/mp4' />
</video>
<center><a href='output/images/$imagefolder/output.mpg' target='_blank'>Descargar</a></center>
";
}
else
{
	print "<a href=\"javascript:openPopUp('output/images/$imagefolder/output.png',960,555)\"><IMG SRC='output/images/$imagefolder/output.png' width='100%'/></a>"
}


