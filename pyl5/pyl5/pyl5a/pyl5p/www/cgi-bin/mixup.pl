
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
		<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>

		<base href='..'>

		<meta name='robots' content='inicio, follow'>
		<meta name='keywords' content=''>
		<meta name='description' content='What symbol can I use?'>
		<meta name='generator' content='Daniel ... con la ayuda de Joomla'>
		<META HTTP-EQUIV='CACHE-CONTROL' CONTENT='NO-CACHE' />
		<META HTTP-EQUIV='Pragma' CONTENT='no-cache' />
		<META HTTP-EQUIV='Expires' CONTENT='0' />

		<title>SBI for Animation for Non-Experts v1.0</title>
		<link rel='stylesheet' href='css/template.css' type='text/css' media='screen,projection'>
		<link rel='stylesheet' href='css/style.css' type='text/css' media='screen,projection'>

		<script type='text/javascript' src='scripts/scripts.js'></script>
		<script type='text/javascript' src='scripts/jquery.js'></script>
		<script type='text/javascript' src='scripts/wz_jsgraphics.js'></script>
		<script type='text/javascript' src='scripts/demo.js'></script>
		
		
		<script type='text/javascript' src='http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js'></script>
		<script type='text/javascript'>
		$(document).ready(function() {
			setTimeout(function() {
				// Grow/Shrink
				$('#menu3 > li > a.expanded + ul').show('normal');
				$('#menu3 > li > a').click(function() {
					$(this).toggleClass('expanded').toggleClass('collapsed').parent().find('> ul').toggle('normal');
				});
				$('#example3 .expand_all').click(function() {
					$('#menu3 > li > a.collapsed').addClass('expanded').removeClass('collapsed').parent().find('> ul').show('normal');
				});
				$('#example3 .collapse_all').click(function() {
					$('#menu3 > li > a.expanded').addClass('collapsed').removeClass('expanded').parent().find('> ul').hide('normal');
				});
			}, 250);
		});
		
		
		</script>
	</head>
	
	
	<body style='font-size: 100%; '>
		<div id='contenedor'>
			<div id='logo'>
				<div class='page_title'>
					<h2 class='logo'>@langMixupTitle</h2>
				</div>
			</div>
		</div>
		<div id='contenedor' style='text-align:center;padding-left:20px;padding-right:20px;'>
			@langMixupText1
			<IMG src='images/@langMixupImg1' width='340px'/><br><br>
		</div><br>";
		
print "
	</body>
</html>
";
