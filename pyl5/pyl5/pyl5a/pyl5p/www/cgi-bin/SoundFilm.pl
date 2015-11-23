
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
my $imagefolder = $query->param("imagefolder");
my $soundsActors = $query->param("soundsActors");
my $soundsAnimations = $query->param("soundsAnimations");

#my $defaultText = GetDefaultActorNumber($imagefolder);
my $defaultText = "";

ExecuteSoundFilm($imagefolder, $defaultText, $defaultText);
