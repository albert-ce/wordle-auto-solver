import sys

default_val = 'res/spanish-dict-5.txt'

def get_frequencies(words):
    # Count how many times each character appears overall and at each position
    freq = {}
    pos_freq = [{},{},{},{},{}]
    for word in words:
        for pos, char in enumerate(word):
            if char not in pos_freq[pos]:
                pos_freq[pos][char] = 1
            else:
                pos_freq[pos][char] = pos_freq[pos][char] + 1
            if char not in freq:
                freq[char] = 1
            else:
                freq[char] = freq[char] + 1
    return freq, pos_freq


def get_scores(words, freq, pos_freq):
    # Assign a score to each word based on character frequencies
    scores = []
    for word in words:
        checked_chars = []
        score = 0
        for pos, char in enumerate(word):
            if char not in checked_chars:
                score = score + freq[char]
                checked_chars.append(char)
            score = score + pos_freq[pos][char]
        scores.append(score)
    return scores


def sort_words(fileName):
    # Get all unique words from the text file and store them in an array
    original_file = open(fileName, 'r', encoding='utf-8')
    words = list(set(original_file.read().splitlines()))

    # Assign a score to each word based on the frequencies of characters
    freq, pos_freq = get_frequencies(words)
    scores = get_scores(words, freq, pos_freq)

    # Sort the words by their score
    merged = list(zip(words, scores))
    merged = sorted(merged, key=lambda x: x[1], reverse=True)
    freq_sorted = [word for word, score in merged]

    # Write the words in order in a new file
    new_file = open(fileName.replace('.txt', '-sorted.txt'), 'w', encoding='utf-8')
    new_file.truncate()
    for word in freq_sorted:
            new_file.write(word+'\n')

if __name__ == '__main__':
    try: 
        sort_words(sys.argv[1] if len(sys.argv)==2 else default_val)
    except:
        print('Error: No such file: \''+sys.argv[1]+'\'')