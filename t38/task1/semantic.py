# import spacy and its English language model
import spacy
nlp = spacy.load("en_core_web_md")

# EXAMPLE 1
word1 = nlp("cat")
word2 = nlp("monkey")
word3 = nlp("banana")

print(word1.similarity(word2))
print(word3.similarity(word2))
print(word3.similarity(word1))

# EXAMPLE 2
tokens = nlp("cat apple monkey banana")
for token1 in tokens:
    for token2 in tokens:
        print(token1.text, token2.text, token1.similarity(token2))

# EXAMPLE 3
sentence_to_compare = "Why is my cat on the car"

sentences = ["where did my dog go",
             "Hello, there is my car",
             "I've lost my car in my car",
             "I'd like my boat back",
             "I will name my dog Diana"]

model_sentence = nlp(sentence_to_compare)

for sentence in sentences:
    similarity = nlp(sentence).similarity(model_sentence)
    print(sentence + " - ", similarity)

# NOTES
    # monkey and banana are more similar that cat and banana
    # shows that the model recognises the connection between monkeys and bananas

# MY EXAMPLE
word1 = nlp("crab")
word2 = nlp("monkey")
word3 = nlp("coconut")
print(word1.similarity(word2))
print(word3.similarity(word2))
print(word3.similarity(word1))
# NOTES
    # crab and coconut are more similar than monkey and coconut
    # the model maybe recognises the connection between coconuts, crabs, and beaches