# Introduction to Data Mining Final Project

Jordan Christiansen, Mark Swam

For our final project, we have decided to evaluate several different data mining techniques on a data set that we consider to be interesting. We will be attempting to classify movie genre based on multiple different numeric characteristics.

To select our data, we used the IMDB alternative interfaces database, which contains lists of hundreds of thousands of movies, as well as large amounts of data for each. From this interface, we selected the three genres with the most available titles. These turned out to be:

1.	Short 	(590,442 titles)

2.	Drama 	(371,663 titles)

3.	Comedy 	(271,300 titles)

For these, we will be evaluating them based on:

* Year of release

* Running time

* Average rating

* Country of origin

* Spoken language

* Director(s) (usually a movie only has one director

* Editors

For the non-numeric data (language and country of origin), we will be assigning binary values (1 or 0) for each column. 

Finally, we will be evaluating our data using the following classification methods:

1.	Naïve Bayesian

2.	Decision Trees

3.	Support Vector Machines

Once we have evaluated our data using the above methods, we will be comparing the results of each and attempting to determine whether or not there is actually a correlation between these different characteristics and the genre. There may be, but there also may not be. That is what we intend to determine. Additionally, we will attempt to determine which of the above characteristics is the most deterministic when it comes to classifying a movie’s genre. 
