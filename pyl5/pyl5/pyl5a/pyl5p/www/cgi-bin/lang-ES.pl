
#Traducción idioma español
#ñ -> &ntilde;
#á -> &aacute;
#é -> &eacute;
#í -> &iacute;
#ó -> &oacute;
#ú -> &uacute;
#(espacio) -> &nbsp;
#(espacio de lina) -> <br>
#@ -> &#64
#¿ -> &iquest;
#' -> &#39;
#" -> &quot;
#- -> &#45;

#template.pl
@langProjectName='Papel y L&aacute;piz<br/>Grupo de Investigaci&oacute;n IMAGINE'; #'Sketch Based Interfaces for Animation for Non-Experts<br/>Research Group IMAGINE';
@langSelectTitleES='Espa&ntilde;ol';
@langSelectImgES='flagES.gif';
@langSelectTitleEN='English';
@langSelectImgEN='flagEN-stop.jpg';
@langHome='Inicio';
@langDavid='D.A.V.I.D.';
@langUserManual='Manual';
@langFAQ='FAQ';
@langFAQ1='&iquest;C&oacute;mo puedo crear mi tarjeta 3D?';
@langFAQ2='&iquest;Qu&eacute; s&iacute;mbolos puedo utilizar?';
@langFAQ3='&iquest;Por qu&eacute; no veo mi personaje?';
@langHelp='Ayuda';
@langHelp1='Acerca';
@langHelp2='Agradecimientos';
@langContact='Cont&aacute;ctanos en:';
@langContactEmail='pyl&#64uniandes.edu.co';
@langErrorOnPreview='Lo lamentamos mucho, ha pasado demasiado tiempo. Por favor intenta mas tarde';

#inicio.pl
@langStep1='Paso 1';
@langBanner='cabezote-es.jpg';
@langStep1Img3='step03-es.jpg';
@langStep1Opt1='1) Puedes subir tu propio boceto...';
@langStep1Tip='El proceso';
@langOr='...&Oacute;...';
@langUpload='Subir';
@langStep1Opt2='2) Puedes seleccionar bocetos precargados...';
@langStep2Tip='Bocetos Precargados';
@langSelect='Seleccionar';
@langError="Ha ocurrido un error. Posibles Causas:<BR/>(1) No seleccionaste un archivo<BR/>(2) El archivo seleccionado es demasiado grande (M&aacute;ximo tama&ntilde;o: 5 MB)";
@langStep2='Paso 2';
@langName='Tu nombre:';
@langDefaultName='';
@langEmail='Enviar e-mail a:';
@langDefaultEmail='';
@langDefaultSubject='te ha enviado una tarjeta animada';
@langMessage='Mensaje:';
@langDefaultMessage='Mira la animaci&oacute;n que hice con el proyecto Papel y L&aacute;piz!';
@langSend='Enviar';
@langErrorMissing='Falta el campo/s:';
@langErrorFormat='Campo inv&aacute;lido/s:';
@langLoadingEmail='Estamos generando tu tarjeta, cuando est&eacute; terminada enviaremos un correo a';
@langTryAgain="Para volver a iniciar dar clic <a href=&#39;cgi-bin/inicio.pl?lang=es&#39;>aqu&iacute;</a>";
@langLoadingPreview='Por favor espere, estamos generando una vista previa...';

#option1help.pl
@langOption1Title='Dibuja tu propio boceto';
@langOption1Img1='step01-es.jpg';
@langOption1Text1='&Eacute;stos son nuestros s&iacute;mbolos:';
@langOption1Text2="Cuando termines, sube tu dibujo:";
@langOption1Img2='step02-es.jpg';

#option2help.pl
@langOption2Title='Bocetos Precargados';

#choose-previows-image.pl
@langPreloadedTitle='Selecciona el boceto que deseas procesar';
@langPreloadedExecute='Recalcular';
@langPreloadedSendMail='Enviar Correo';

#about.pl
@langAboutTitle='Acerca de nosotros';
@langAboutText1='El proyecto de Papel y l&aacute;piz hace parte del proyecto D.A.V.I.D el cual es financiado por Colciencias. 
El proyecto Papel y L&aacute;piz presenta una interfaz que basada en bocetos, permite a cualquier usuario crear una animaci&oacute;n 
3D a partir de un boceto a l&aacute;piz y papel. Esta interfaz es una herramienta para la creaci&oacute;n de animaciones 3D de manera r&aacute;pida y sencilla.<br><br>

<b>Integrantes Actuales:</b><br><br>
<b>Pablo Figueroa / Director</b><br>
pfiguero@uniandes.edu.co<br><br>

<b>Julian Arcos / Ing. Sistemas &#45; Programador</b><br>
je.arcos31@uniandes.edu.co<br><br>

<b>Juan Manuel Moreno / Ing. Sistemas &#45; Programador</b><br>
jm.moreno743@uniandes.edu.co<br><br>

<b>Diego Rodr&iacute;guez / Ing. Sistemas &#45; Programador</b><br>
jm.moreno743@uniandes.edu.co<br><br>

<b>David D&iacute;az / Dise&ntilde;ador</b><br>
ds.diaz@uniandes.edu.co<br><br>

<b>Integrantes Antiguos:</b><br>Agustin Conde y Daniel Wilches.';

#acknowledge.pl
@langAckTitle='Agradecimientos';
@langAckText1='<b>Colciencias<br><br>
Fundaci&oacute;n Rafael Pombo<br><br>
DVO Universal Brands<br><br>
Proyecto David<br><br>
Colombia Games - E-nnova - Oruga Touching Dreams - Quantica Music.</b>';

#create.pl
@langCreateTitle='&iquest;C&oacute;mo puedo crear my tarjeta 3D?';
@langCreateIntro='Hay dos formas de crear una tarjeta 3D. La primera es crear tu propio boceto utilizando los s&iacute;mbolos soportados y subirlo a nuestro portal.<br><br>';
@langCreateText1='<b>Subir un dibujo a nuestro portal:</b><br>Primero da clic en Seleccionar Archivo.<br>';
@langCreateText2='Busca tu dibujo y da clic en abrir.<br>';
@langCreateText3='Da clic en Subir.<br>';
@langCreateText4='Listo!!!<br><br>La segunda forma de generar una tarjeta 3D es utilizar un boceto precargado.<br><br><b>Utilizar un boceto precargado</b><br>Primero da clic en Seleccionar.<br>';
@langCreateText5='Ubica el boceto que quieres utilizar y da clic en Ejecutar.<br>';
@langCreateText6='Listo!!!<br><br>A continuaci&oacute;n se mostrar&aacute; la imagen que elegiste y nuestro portal empezar&aacute; a procesarla.<br>';
@langCreateText7='Cuando termine ver&aacute;s una vista previa de tu boceto.<br>';
@langCreateText8='Y si lo deseas puedes enviar los resultados de tu boceto (imagen y video) por correo, solo ingresa los datos pedidos y da clic en Enviar.<br>';
@langCreateText9='Nuestro portal se encargar&aacute; del resto.<br>';
@langCreateImg1='createP01-es.jpg';
@langCreateImg2='createP02-es.jpg';
@langCreateImg3='createP03-es.jpg';
@langCreateImg4='createP04-es.jpg';
@langCreateImg5='createP05-es.jpg';
@langCreateImg6='createP06-es.jpg';
@langCreateImg7='createP07-es.jpg';
@langCreateImg8='createP08-es.jpg';
@langCreateImg9='createP09-es.jpg';

#symbol.pl
@langSymbolTitle='&iquest;Qu&eacute; s&iacute;mbolos puedo utilizar?';
@langSymbolText1='&Eacute;stos son nuestros s&iacute;mbolos:';

#mixup.pl
@langMixupTitle='&iquest;Por qu&eacute; no veo mi personaje?';
@langMixupText1='En algunos casos nuestro portal no puede identificar un s&iacute;mbolo dibujado por lo que &eacute;ste s&iacute;mbolo se mostrar&aacute; como un Sackboy<br><br>';
@langMixupImg1='mixup.jpg';
