#!/usr/bin/perl

#use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use URI::Escape;
use Data::Dumper;
use File::Copy;
use Digest::MD5;

require 'paths.pl';
require 'template.pl';
require 'functions.pl';

$| = 1;

my $query = new CGI;
my $DISABLE = "disabled='disabled'";
my $SESSION_DIR = "";
##########################
my $error = $query->param("error");
my $imagename = $query->param("imagename");
my $uploaddir = $query->param("uploaddir");
my $lang = $query->param("lang");

if($lang eq 'es'){
	require 'lang-ES.pl';
}else{
	$lang = 'en';
	require 'lang-EN.pl';
}

my $recognizedImage = "<IMG src='images/recognized.png' width='60%'/>";
my $renderimage = "<IMG src='images/renderimage.png' width='60%'/>";

if ($imagename){
	$DISABLE = "";
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

	$SESSION_DIR = $md5_checksum;

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
	
	$recognizedImage="<IMG SRC='output/images/$SESSION_DIR/Processing_$imagename' id='imagen' width='100%'/>";
	
	
	$renderimage =
"<div id='imagePreview' width='100%'>
	<A href='#'><IMG src='images/kreski/gnome-settings'/><br>ERROR :(</A>
</div>";
}




#################

BeginPage($lang,"", $SESSION_DIR,$imagename);

print "
<div>
	<IMG src='images/@langBanner' width='100%' style:'float:left;'/>
</div>";

BeginSection(@langStep1, "sect_1_div");
print "
<div id='' style='text-align:center;'>
	<table align='center' width='100%'>
		<tr>
			<td align='left' width='60%'> <IMG src='images/@langStep1Img3' width='100%' style:'float:left;'/></td>
			<td width='40%'>
				<table align='left' width='100%' class='center_tds'>
					<tr>
						<td colspan='2' ><b>&nbsp;</b></td>
					</tr>
					
					<form action='cgi-bin/upload.pl' method='post' enctype='multipart/form-data'>
						<tr>
							<td align='left' width='70%'><font size='2'>@langStep1Opt1</font></td>
							<td align='left' width='30%'>
								<a href=\"javascript:openPopUp('cgi-bin/option1help.pl?lang=$lang',600,300)\" title='@langStep1Tip'><IMG src='images/question-mark.jpg' width='25px' style:'float:left;'/></a>
							</td>
						</tr>
						<tr>
							<td align='left' colspan='2'>
								<input lang='en' type='file' name='photo' accept='image/*' size=10/>
								<input type='hidden' value='$lang' name='lang' />
							</td>
						</tr>
						<tr>
							<td align='center' colspan='2'> <input type='submit' name='Submit' value='@langUpload'/> </td>
						</tr>
					</form>
					<tr>
						<td colspan='2' ><b><font size='2'>@langOr</font></b></td>
					</tr>
					<tr>
						<td align='left'><font size='2'>@langStep1Opt2</font></td>
						<td align='left'>
							<a href=\"javascript:openPopUp('cgi-bin/option2help.pl?lang=$lang',650,400)\" title='@langStep2Tip'><IMG src='images/question-mark.jpg' width='25px' style:'float:left;'/></a>
						</td>
					</tr>
					<tr>
						<td colspan='2'>
						<input onclick=\"javascript:openPopUp('cgi-bin/choose-previows-image.pl?lang=$lang',650,400)\" type='submit' name='Submit' value='@langSelect' />
						</td>
					</tr>
				</table>
				
				
			</td>
		</tr>
	</table>
</div>";

if ($error){
	print "<P class='error'>@langError</P>";
}

EndSection();


					
BeginSection(@langStep2, "sect_2_div");
print "
<div id='' style='text-align:center;' width='960px'>
	<table align='center' width='960px' >
		<tr>
			<td width='60%'>
			
				<table width='100%' align='left'>
					<tr>
						<td width='40%' style='border:1px solid black;'>
							$recognizedImage
						</td>
						<td width='20%'>
							<IMG src='images/flechader.png' width='60%' />
						</td>
						<td style='border:1px solid black;'>
							$renderimage
						</td>
					</tr>
				</table>
				
			</td>
			<td width='40%'>
				<div id='mailForm' width='100%'>
					<table align='center'>
						<tr>
							<!-- td>@langName<br/> <input onclick='this.value=\"\";' type='text' id='nombrede' value='@langDefaultName' $DISABLE></td -->
							<td>@langName<br/> <input type='text' id='nombrede' value='@langDefaultName' $DISABLE></td>
							<td>@langEmail<br/> <input type='text' id='mailpara' value='@langDefaultEmail' $DISABLE></td>
						</tr>
						<tr>
							<td colspan='2'>@langMessage<br/> <textarea id='atext' rows='10' cols='40' $DISABLE>@langDefaultMessage</textarea> </td>
						</tr>
						<tr>
							<td colspan='2' align='center'><input onclick='initMailProcessing(\"False\",\"True\", \"$SESSION_DIR\", \"@langDefaultSubject\", \"@langName\", \"@langEmail\", \"@langMessage\", \"@langErrorMissing\", \"@langErrorFormat\", \"@langLoadingEmail\", \"@langTryAgain\");'
														type='submit' name='Submit' value='@langSend' $DISABLE/></td>
						</tr>
					</table>
				</div>
			</td>
		</tr>
	</table>
	
</div>
";
EndSection();

EndPage($lang);
