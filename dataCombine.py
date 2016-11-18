import os.path
import re
import sys

# Input files:
movieFile = 'data/genres.list'
dataFiles = [
        'data/countries.list',
        'data/language.list',
        'data/running-times.list',
        'data/ratings.list',
        'data/directors.list']

########################################
# Construct our data from the sources. #
########################################

# These are the genres that we are studying.
analyzedGenres = ['Drama', 'Comedy', 'Documentary']
data = []

# Compile the regex patterns for the movie attributes.
titleRE = re.compile(r'(?P<title>.+) \((?P<year>\d+)\S*\)')
res = {
    'generic' : re.compile(r'(?P<title>.+) \(\d+\S*\).*\s+(?P<field>\w+)(?:\s+\(.+\))*$'),
    'time' : re.compile(r'(?P<title>.+) \(\d+\S*\)\s+(?P<field>\d+)(?:\s+\(.+\))*$'),
    'rating' : re.compile(r'^\s+[0-9.*]+\s+[0-9]+\s+(?P<field>[0-9.]+)\s+(?P<title>\S.+) \(\d+\S*\)')
}

with open(movieFile, encoding='iso-8859-1') as movieList:
    i = 0 # for debugging
    for line in movieList:
        # debug
        i += 1
        if i == 500:
            break
        # end debug

        title = ''
        year = ''
        genre = ''

        titleMatch = titleRE.match(line)
        genreMatch = res['generic'].search(line)

        if titleMatch:
            title = titleMatch.group('title')
            year = titleMatch.group('year')
        if genreMatch:
            genre = genreMatch.group('field')

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
                'director' : '',
                'language' : '',
                'time' : '',
                'rating' : '',
            })

print('Collected ' + str(len(data)) + ' movies.', file=sys.stderr)

fields = ['country', 'language', 'time', 'rating']
for i in range(0, len(fields)):
    with open(dataFiles[i], encoding='iso-8859-1') as dataFile:
        lastTitle = ''
        for movie in data:
            # Read through the file until we find the data for the current movie.
            startPosition = dataFile.tell()
            while True:
                line = dataFile.readline()

                # Give up on this movie if we reach the end of the file.
                if line == '':
                    dataFile.seek(startPosition)
                    break

                try:
                    match = res[fields[i]].search(line)
                except KeyError:
                    match = res['generic'].search(line)

                if match:
                    if match.group('title') == movie['title']:
                        fieldData = match.group('field')
                        movie[fields[i]] = fieldData
                        lastTitle = title
                        break
                    elif match.group('title') > movie['title']:
                        # We've passed the movie we're looking for. Give up.
                        dataFile.seek(startPosition)
                        break

        print('Finished collecting ' + fields[i] + '...', file=sys.stderr)

# Find the director for each movie.


#################################
# Write the data out to a file. #
#################################

print(file=sys.stderr)

headerString = 'Title\tYear\tCountry\tLanguage\tRunning time\tRating\tGenre'
print(headerString)
for movie in data:
    outputString = '\t'.join([
        movie['title'],
        movie['year'],
        movie['country'],
        movie['language'],
        # movie['director'],
        str(movie['time']),
        str(movie['rating']),
        movie['genre']
    ])

    print(outputString)
