
#!/usr/bin/perl

#use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use URI::Escape;

my $query = new CGI;
my $error = $query->param("error");
my $IMAGE_TEST = '../images/prueba';

require 'template.pl';
require 'functions.pl';

BeginPage("&nbsp;");

BeginSection("Symbol set in use", "symbolset_div", "fullwidth_div");

PrintSymbolSet();

EndSection();

BeginSection("Upload an image", "upload-image");

print "
<div id='uploadformulary'>
<IMG src='images/kreski/file-manager' />
<table width='80%' align='center' class='center_tds'>
       <form action='cgi-bin/upload.pl' method='post' enctype='multipart/form-data'>
               <tr><td>Select a file from your computer:</td></tr>
               <tr><td><input type='file' name='photo' /></td></tr>
               <tr><td><input type='submit' name='Submit' value='Start uploading' /></td></tr>
       </form>
       </table>
</div>
";

if ($error)
{
	print "<P class='error'>An error has occurred. Posible causes:<BR/>" .
		"(1) You didn't select any file<BR/>" .
		"(2) The selected file was too big (maximum filesize is 5 Mb)</P>";
}


EndSection();

EndPage();
