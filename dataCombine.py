import gzip
import os.path
import re
import sys
import urllib.request

movieFile = 'data/genres.list.gz'
dataFiles = [
        'data/countries.list.gz',
        'data/language.list.gz',
        'data/running-times.list.gz',
        'data/ratings.list.gz',
        'data/directors.list.gz',
        'data/writers.list.gz']

# Output file:
workingDir = os.path.dirname(os.path.realpath(__file__)) + '/'
if len(sys.argv) == 2:
    outputFile = sys.argv[1]
else:
    outputFile = workingDir + 'movies.tsv'

########################################
# Construct our data from the sources. #
########################################

# These are the genres that we are studying.
analyzedGenres = ['Drama', 'Comedy', 'Documentary']
data = []

# Compile the regex patterns for the movie attributes.
titleRE = re.compile(r'(.+) \((\d+)\S*\)')
res = {
    'generic' : re.compile(r'.+ \(\d+\S*\).*\s+(\w+)(\s+\(.+\))*$'),
    'time' : re.compile(r'.+ \(\d+\S*\).*(\d+)(\s+\(.+\))*$'),
    'ratings' : re.compile(r'^\s+[0-9.]+\s+[0-9]+\s+([0-9.]+)')
}

# with gzip.open(urllib.request.urlopen(movieFile)) as movieList:
with open('/home/jordan/Downloads/genres.list', encoding='iso-8859-1') as movieList:
    i = 0 # for debugging
    for line in movieList:
        # debug
        i += 1
        if i == 500:
            break
        # end debug

        # line = line.decode('iso-8859-1')

        title = ''
        year = ''
        genre = ''

        titleMatch = titleRE.match(line)
        genreMatch = res['generic'].search(line)

        if titleMatch:
            title = titleMatch.group(1)
            year = titleMatch.group(2)
        if genreMatch:
            genre = genreMatch.group(1)

        # Skip if:
        # This movie isn't in one of the genres we're interested in.
        # This is a duplicate entry.
        if not genre in analyzedGenres \
            or len(data) > 0 and title == data[-1]['title']:
            continue

        if len(title) > 0:
            data.append({
                'title': title,
                'year': year,
                'genre': genre,
                'country' : '',
                'language' : '',
                'time' : -1,
                'rating' : -1,
                'directors' : {},
                'writers' : {}
            })

print('Collected ' + str(len(data)) + ' movies.')

fields = ['country', 'language', 'time', 'rating', 'directors', 'writers']
for i in range(0, 4):
    dbSeek = 0
    with gzip.open(urllib.request.urlopen(dataFiles[i])) as dataFile:
        for line in dataFile:
            line = line.decode('iso-8859-1')

            try:
                match = res[fields[i]].search(line)
            except KeyError:
                match = res['generic'].search(line)

            if match:
                title = titleRE.match(line).group(1)
                fieldData = match.group(1)

                try:
                    while data[dbSeek][fields[i]]:
                        dbSeek += 1

                    while title != data[dbSeek]['title']:
                        dbSeek += 1

                    data[dbSeek][fields[i]] = fieldData
                except IndexError:
                    print('Finised collecting ' + fields[i] + '...')
                    break

# Find the each movie's director.


#################################
# Write the data out to a file. #
#################################
print('Title\tYear\tCountry\tLanguage\tRunning time\tRating\tGenre')
for movie in data:
    outputString = '\t'.join([
        movie['title'],
        movie['year'],
        movie['country'],
        movie['language'],
        str(movie['time']),
        str(movie['rating'])
    ])

    # outputString = '\t'.join([outputString] + movie['directors'])
    # outputString = '\t'.join([outputString] + movie['writers'])

    outputString = '\t'.join([outputString, movie['genre']])

    print(outputString)
