#!/bin/bash

urls=('ftp://ftp.fu-berlin.de/pub/misc/movies/database/genres.list.gz'\
    'ftp://ftp.fu-berlin.de/pub/misc/movies/database/countries.list.gz'\
    'ftp://ftp.fu-berlin.de/pub/misc/movies/database/language.list.gz'\
    'ftp://ftp.fu-berlin.de/pub/misc/movies/database/running-times.list.gz'\
    'ftp://ftp.fu-berlin.de/pub/misc/movies/database/ratings.list.gz'\
    'ftp://ftp.fu-berlin.de/pub/misc/movies/database/directors.list.gz')

if [ ! -d data ]; then
    mkdir data
fi

for url in ${urls[@]}; do
    file=$(echo $url | grep -Eo '[a-z-]+\.list')
    curl $url | gunzip > "data/$file"
done

# Remove garbage at the beginning of files.
sed -i '1,296d' data/ratings.list
sed -i '1,235d' data/directors.list
