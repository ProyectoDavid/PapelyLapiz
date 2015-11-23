
#!/usr/bin/perl
use CGI;

require 'template.pl';
require 'functions.pl';

my $query = new CGI;
my $lang = $query->param("lang");

if($lang eq 'es'){
	require 'lang-ES.pl';
}else{
	require 'lang-EN.pl';
}

print "

<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='es-es' lang='es-es' dir='ltr'>
	<head>
		<meta http-equiv='Content-Type' content='application/pdf'>
	</head>
	
	<body style='font-size: 100%; '>
		<object data="http://papelylapiz.virtual.uniandes.edu.co/pyl5/www/cgi-bin/manual_es.pdf" type="application/pdf" width="100%" height="100%">
		</object>		
	</body>
</html>
";

print "Content-type: application/pdf;\n\n";
