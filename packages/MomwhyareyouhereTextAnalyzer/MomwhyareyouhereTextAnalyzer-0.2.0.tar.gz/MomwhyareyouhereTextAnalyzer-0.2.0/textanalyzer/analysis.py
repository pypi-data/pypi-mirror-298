import re

def word_count(text):
    words = text.split()
    return len(words)

def character_count(text):
    return len(text)

def sentence_count(text):
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def readability_score(text):
    words = word_count(text)
    sentences = sentence_count(text)
    syllables = sum(count_syllables(word) for word in text.split())

    if sentences == 0 or words == 0:
        return 0.0
    
    score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    return score

def count_syllables(word):
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    if word[0] in vowels:
        count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count = 1
    return count