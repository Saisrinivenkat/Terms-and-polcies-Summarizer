from nltk.tree import Tree
from nltk.parse.stanford import StanfordParser
from math import sqrt
from parser import tree_to_sentence

class SentenceCompress:
	def __init__(self, word_bank=None):
		self.parser = StanfordParser()
		self.omega = 0.001 
		self.alpha = 50 
		self.beta = 500 
		self.parsed_sentences = None
		self.word_bank = word_bank

	def syntax_parse(self, sentences):
		self.parsed_sentences = self.parser.raw_parse_sents([s.sentence for s in sentences])

	def compress(self):
		
		compressed_sentences = []
		for list_iter in self.parsed_sentences:
			for t in list_iter:
				original = tree_to_sentence(t)
				min_len = min(len(original), self.alpha)
				max_len = self.max_length(original)

				if len(original) >= min_len: 
					t = self.remove_waste_words(t, max_len)
					s = tree_to_sentence(t) 
					compressed_sentences.append(s)
		return compressed_sentences

	def word_significance(self, w): 
		if w in self.word_bank.word_dict:
			word = self.word_bank.word_dict[w]
			if w[0].islower(): 
				return word.tf * word.idf 
			elif w[0].isupper(): 
				return word.tf * word.idf + self.omega 
		return 0 

	def max_length(self, sentence):
		orig_length = len(sentence)
		if orig_length > self.beta:
			return self.beta + sqrt(orig_length - self.beta)
		return orig_length


	def remove_waste_words_find_xp_levels(self, tree, decl_clause, level, found_xp):
		max_levels = level
		for index, node in enumerate(tree):
			if type(node) == Tree:
				if index == 0 and node.label() == decl_clause:
					found_xp = True
					levels = self.remove_waste_words_find_xp_levels(node, decl_clause, level+1, found_xp)
					max_levels = max(levels, max_levels)
				elif not found_xp: 
					levels = self.remove_waste_words_find_xp_levels(node, decl_clause, level, found_xp)
		return max_levels

	def remove_waste_words_remove_outer_xp(self, tree, decl_clause):
		for node in tree:
			if type(node) == Tree:
				if node.label() == decl_clause:
					for index2, child_node in enumerate(node):
						if type(child_node) == Tree and child_node.label() == decl_clause:
							return node[index2]
				else:
					subtree = self.remove_waste_words_remove_outer_xp(node, decl_clause)
					if subtree is not None:
						return subtree
		return None 

	def remove_waste_words_trailing(self, tree, phrase_type):
		for index, node in reversed(list(enumerate(tree))):
			if type(node) == Tree:
				if index == len(tree)-1 and node.label() == phrase_type and self.clause_significance(node) < 0.01:
					tree[index] = None
					return True
				else:
					found = self.remove_waste_words_trailing(node, phrase_type)
					if found:
						return True
		return False

	def remove_waste_words(self, tree, max_len):
		XPs = ['S', 'NP', 'VP']
		for clause in XPs:
			current_sentence_len = len(tree_to_sentence(tree))
			if (current_sentence_len < max_len):
				break
			levels = self.remove_waste_words_find_xp_levels(tree, clause, 0, False)
			while levels > 1:
				current_sentence_len = len(tree_to_sentence(tree))
				if (current_sentence_len < max_len):
					break
				tree = self.remove_waste_words_remove_outer_xp(tree, clause)
				levels = self.remove_waste_words_find_xp_levels(tree, clause, 0, False)
		trailing = ['PP', 'SBAR']
		for phrase in trailing:
			current_sentence_len = len(tree_to_sentence(tree))
			if (current_sentence_len < max_len):
				break
			self.remove_waste_words_trailing(tree, phrase)
		return tree

	def clause_significance(self, tree):
		clause_sig = 0
		for index, node in enumerate(tree):
			if type(node) == Tree:
				clause_sig += self.clause_significance(node) 
			else:
				clause_sig += self.word_significance(node)
		return clause_sig

	


