
#!/usr/bin/perl

require 'template.pl';
require 'functions.pl';

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
					<h2 class='logo'>How can I store/send a created 3D card?</h2>
				</div>
			</div>
		</div>
		<div id='contenedor'>
		Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Morbi eu tortor vel neque congue congue. Mauris quis erat. Vestibulum dictum ligula vel purus. Vivamus eget purus. Quisque nulla. Proin nonummy elit nec erat. Suspendisse molestie, orci sed molestie congue, erat pede consectetuer tellus, non ultricies turpis purus eget lorem. Fusce ut libero. Donec gravida euismod elit. Sed rhoncus. Vivamus nibh magna, scelerisque id, tempus in, auctor non, ipsum. Vivamus vitae metus id elit consectetuer vestibulum. Etiam augue. Ut velit urna, porta a, commodo vitae, blandit vitae, odio. Ut mi arcu, placerat eu, imperdiet non, molestie quis, elit. Phasellus ligula ipsum, venenatis sit amet, feugiat eget, blandit aliquam, risus. Donec mollis.
		</div>
		
	</body>
</html>
";
