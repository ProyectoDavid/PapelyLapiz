#
#Papel y Lapiz - Software para la creacion de pequeños cortos.
#Copyright (C) 2015  Universidad de Los Andes - Proyecto DAVID.   
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation,
#Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#!/usr/bin/perl
##
##  printenv -- demo CGI program which just prints its environment
##

print "Content-type: text/plain; charset=iso-8859-1\n\n";

foreach $var (sort(keys(%ENV))) {
    $val = $ENV{$var};
    $val =~ s|\n|\\n|g;
    $val =~ s|"|\\"|g;
    print "${var}=\"${val}\"\n";
}

print `whoami`;
