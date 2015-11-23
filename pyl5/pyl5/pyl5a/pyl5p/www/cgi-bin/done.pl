
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

my $query = new CGI;
my $imagename = $query->param("imagename");
my $uploaddir = $query->param("uploaddir");

my $THESIS_DIR = "$ROOT_PATH/ImageProcessing";
my $GENERATED_DIR = "$THESIS_DIR/Execution/Log";
my $IMAGE_TEST = "$WEB_ROOT_PATH/images/prueba";
my $UPLOAD_DIR = $uploaddir eq "" ? $TEMP_PATH : "$WEB_ROOT_PATH/output/images/$uploaddir";


# Genero una identificacion unica para esta imagen
$md5 = Digest::MD5->new;
open TMP_FILE, "$UPLOAD_DIR/$imagename";
$md5->addfile(TMP_FILE);
$md5_checksum = $md5->hexdigest;
close TMP_FILE;

my $SESSION_DIR = $md5_checksum;

# copiar al directorio accesible por Apache la imagen que el usuario subio
mkdir "$GENERATED_DIR/$SESSION_DIR";

if ($imagename =~ 'Processing_')
{
	copy "$UPLOAD_DIR/$imagename", "$GENERATED_DIR/$SESSION_DIR/$imagename";
	$imagename =~ s/Processing_//;
}
else
{
	copy "$UPLOAD_DIR/$imagename", "$GENERATED_DIR/$SESSION_DIR/Processing_$imagename";
}

BeginPage("You can click on the section titles to hide/show the contents", $SESSION_DIR);

BeginSection("Symbol set in use", "symbolset_div", "fullwidth_div");

PrintSymbolSet();

EndSection();

BeginSection("Choosen image ($imagename)", "choosen_image_div");

print "
	<div id='scroll'>
		<center>
			<A onClick='cambiarTamanoImagen()'>
				<IMG SRC='images/recuadro.png' id='recuadro'
					style='z-index:10; position:absolute; visibility:hidden;' />

				<IMG SRC='output/images/$SESSION_DIR/Processing_$imagename' id='imagen'
					style='position:relative; top: 0px; left: 0px; z-index: 1;' />
			</A>
		</center>
	</div>
		
	<script type='text/javascript'>
		cambiarTamanoImagen();
	
		\$('#scroll').scroll(function()
		{
			\$('#recuadro').css('visibility','hidden');
		});
	</script>
";

EndSection();


BeginSection("1. Image processing", "sect_1_div");

print "
<div id='executeResponse'>
<A onclick='executeImageProcessing(\"$SESSION_DIR\", \"Processing_$imagename\");alert(\"listo para soundfilm\");executeSoundFilm(\"$SESSION_DIR\");'>
	<IMG src='images/kreski/gnome-settings' /><br/>Click in this icon to start the recognition process</A>
</div>
";

EndSection();

print "<div id='executeResponse2'></div> ";

print "<div id='videoResponse' style='visibility:hidden; display:none'>";

BeginSection("2. Image rendering", "sect_2_div");

print "
<div id='videoResponse2'>
                        <A onclick='executeVideoGenerator(\"True\",\"False\", \"$SESSION_DIR\")'><IMG src='images/kreski/gnome-settings' /><br/>
				Click in this icon to start rendering the image
			</A>
</div>
";

EndSection();

BeginSection("3. Video rendering", "sect_3_div");

print "
<div id='videoResponse3'>
                        <A onclick='executeVideoGenerator(\"False\",\"True\", \"$SESSION_DIR\")'><IMG src='images/kreski/gnome-settings' /><br/>
				Click in this icon to start rendering the video
			</A>

</div>
";

EndSection();

print "</div>";

EndPage();

