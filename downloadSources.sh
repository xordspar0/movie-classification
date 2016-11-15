#!/bin/bash

urls=('ftp://ftp.fu-berlin.de/pub/misc/movies/database/genres.list.gz'\
    'ftp://ftp.fu-berlin.de/pub/misc/movies/database/countries.list.gz'\
    'ftp://ftp.fu-berlin.de/pub/misc/movies/database/language.list.gz'\
    'ftp://ftp.fu-berlin.de/pub/misc/movies/database/running-times.list.gz'\
    'ftp://ftp.fu-berlin.de/pub/misc/movies/database/ratings.list.gz'\
    'ftp://ftp.fu-berlin.de/pub/misc/movies/database/directors.list.gz'\
    'ftp://ftp.fu-berlin.de/pub/misc/movies/database/writers.list.gz')

if [ ! -d data ]; then
    mkdir data
fi

for url in $urls; do
    curl $url | gunzip > "data/${url##ftp://*/}"
done
