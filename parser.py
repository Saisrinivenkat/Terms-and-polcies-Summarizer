from  nltk import sent_tokenize,word_tokenize,Tree
import string

def token_sent(data):
    return sent_tokenize(data)

def token_words(sentence):
    return word_tokenize(sentence)


def parse_stop_words(filename):
	with open(filename, 'r') as f:
		data = f.readlines()
	return [stop_word.strip() for stop_word in data]


def word_tokenize_tos(full_sentences):
	return [word_tokenize(s) for s in full_sentences]


def word_tokenize_sent(full_sentence):
	return word_tokenize(full_sentence)

def tree_to_sentence_helper(tree, sentence_str):
		for index, node in enumerate(tree):
			if type(node) == Tree:
				sentence_str = tree_to_sentence_helper(node, sentence_str)
			elif node != None:
				if node[0] in string.punctuation:
					return sentence_str + node
				else:
					return sentence_str + ' ' + node
		return sentence_str

def tree_to_sentence(tree):
	s = tree_to_sentence_helper(tree, '').strip()
	if len(s) == 0:
		return s
	if s[0] in string.punctuation:
		s = s.lstrip(string.punctuation)
	if len(s) == 0:
		return s
	if s[0].islower():
		s = s[0].upper() + s[1:]
	if s[-1] not in string.punctuation:
		s = s + '.'
	return s