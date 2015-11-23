
#!/usr/bin/perl

#use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use Data::Dumper;
use File::Copy;
use Digest::MD5;

require 'paths.pl';
require 'template.pl';
require 'functions.pl';

$| = 1;


BeginPage("You can click on the section titles to hide/show the contents", $SESSION_DIR);

BeginSection("Symbol set in use", "symbolset_div", "fullwidth_div");

PrintSymbolSet();

EndSection();

EndPage();

