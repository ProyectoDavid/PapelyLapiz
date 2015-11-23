
#!/bin/bash

# Parameters:
{

date

echo Parameter 1: "$1"
echo Parameter 2: "$2"
echo Parameter 3: "$3"
echo Parameter 4: "$4"
echo Parameter 5: "$5"
echo Parameter 6: "$6"
echo Parameter 7: "$7"

echo
cd $7

./MySoundFilm "$1" "$2" "$3" "" ""

#cd $4/SoundFilm
#/var/www/pyl5/ImageProcessing/SoundFilm/MySoundFilm "$1" "$2" "$3" "$6" "$7"

echo
date

} > "$5" 2>&1

