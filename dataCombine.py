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
    for line in movieList:
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

        # # End early, for debugging.
        # if len(data) >= 10000:
        #     break
        #
print('Collected ' + str(len(data)) + ' movies.', file=sys.stderr)

fields = ['country', 'language', 'time', 'rating']
for i in range(0, len(fields)):
    with open(dataFiles[i], encoding='iso-8859-1') as dataFile:
        print('Collecting ' + fields[i] + '...', file=sys.stderr)
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

        print('\tdone.', file=sys.stderr)

# Find the director for each movie.
directorRE = re.compile(r'(?P<director>[\S ]+)\t+(?P<title>[\S ]+) \(.+\)')
movieRE = re.compile(r'\t\t\t(?P<title>.*) \(\S+\)')
print('Collecting director...', file=sys.stderr)
with open(dataFiles[4], encoding='iso-8859-1') as dataFile:
    currentDirector = ''
    for line in dataFile:
        directorMatch = directorRE.match(line)
        foundTitle = ''
        if directorMatch:
            currentDirector = directorMatch.group('director')
            foundTitle = directorMatch.group('title')
        else:
            movieMatch = movieRE.match(line)
            if movieMatch:
                foundTitle = movieMatch.group('title')

        if foundTitle:
            try:
                movie = next((movie for movie in data if movie['title'] == foundTitle))
                movie['director'] = currentDirector
            except StopIteration:
                pass
print('\tdone.', file=sys.stderr)

# Remove any movies with missing data.
for i in range(len(data)-1, -1, -1):
    if '' in data[i].values():
        data.pop(i)

#################################
# Write the data out to a file. #
#################################

print(file=sys.stderr)

headerString = 'Title\tYear\tCountry\tLanguage\tDirector\tRunning time\tRating\tGenre'
print(headerString)
for movie in data:
    outputString = '\t'.join([
        movie['title'],
        movie['year'],
        movie['country'],
        movie['language'],
        movie['director'],
        str(movie['time']),
        str(movie['rating']),
        movie['genre']
    ])

    print(outputString)
