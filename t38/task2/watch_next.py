import spacy


# returns title of movie with the most similar description
def best_match(description):
    # set the language model
    nlp = spacy.load("en_core_web_md")

    # pass description through the model
    description = nlp(description)

    # dictionary of titles: nlp(descriptions)
    movies = {}
    # fill dictionary from txt file
    with open("movies.txt", "r") as f:
        # each line separates the title and description by " :", so split each line by the first occurence of ": "
        # in the resulting list, [0] is the title and [1] the description
        # add these to the dictionary
        for line in f:
            movies[line.strip("\n").split(" :", 1)[0]] = nlp(line.strip("\n").split(" :", 1)[1])

    # initialise the maximum similarity to -1 and the movie name of the best match to None
    max_similarity = -1
    movie_name = None

    # loop through all movies, and keep track of the movie_name which has the highest similarity
    for key in movies:
        if movies[key].similarity(description) > max_similarity:
            max_similarity = movies[key].similarity(description)
            movie_name = key

    # return the movie name of the most similar movie
    return movie_name


# set the description to analyse and call best_match
def main():
    description = "Will he save their world or destroy it? When the Hulk becomes too dangerous for the Earth, the Illuminati trick Hulk into a shuttle and launch him into space to a planet where the Hulk can live in peace. Unfortunately, Hulk land on the planet Sakaar where he is sold into slavery and trained as a gladiator."
    print(best_match(description))


main()