from parser import token_words,word_tokenize_sent
from model import Sentence,WordBank
from sentence_compress import  SentenceCompress
from lexrank import Summarizer
import re


class Model_Summary():
  def __init__(self,sent_tokens):
    self.sentences = list()
    for i, sentence in enumerate(sent_tokens):
        words = token_words(sentence)
        self.sentences.append(Sentence(sentence, words, i))
    
    self.word_bank = WordBank(self.sentences)
  
  def __repr__(self):
        s = ""
        for sentence in self.sentences:
            s += str(sentence) + "\n"
        return s

  def rank_sentences(self):
      sent_matrix = list()
      for sentence in self.sentences:
          words = sentence.word_list()
          sent_matrix.append(words)
      summarizer = Summarizer()
      summarizer.create_graph(sent_matrix)
      scores = summarizer.power_method()
      for i in range(0, len(self.sentences)):
          self.sentences[i].rank = scores[i]

  def common_words(self, top_n):
        return self.word_bank.top(top_n)

  def compress_sentences(self):
      compressor = SentenceCompress(word_bank=self.word_bank)

      compressor.syntax_parse(self.sentences) 

      sentences = compressor.compress()
      self.sentences = []
      for i, sentence in enumerate(sentences):
          if len(sentence) > 0:
              words = word_tokenize_sent(sentence)
              self.sentences.append(Sentence(sentence, words, i))

  def top_sent(self, num):
        sent_rank = list()
        for sentence in self.sentences:
            sent_rank.append((sentence, sentence.rank))
        top_rank = sorted(sent_rank, key=lambda x: x[1], reverse=True)[0:num]
        order_top = [x[0] for x in top_rank]
        return order_top

  def keyword_summary(self, keyword):
      summary = list()
      for sentence in self.sentences:
          match = re.search(keyword, sentence.sentence, flags=re.IGNORECASE)
          if match is not None:
              summary.append(sentence)
      return summary
  
  def rake_sentences(self, maxWords=5):
      for sentence in self.sentences:
        sentence.rake_sentence(maxWords=maxWords)

  def top_keyword_sent(self, num):
      sent_rank = list()
      for sentence in self.sentences:
          sent_rank.append((sentence, sentence.keywords_rank))

      top_rank = sorted(sent_rank, key=lambda x: x[1], reverse=True)[0:num]
      order_top = [x[0] for x in top_rank]
      return order_top
  
  def shorten(self, percentage):
        if percentage < 0.01 or percentage > 1:
            print("Invalid Percentage")
            return
        ranks = [sentence.rank for sentence in self.sentences]
        threshold = sorted(ranks, reverse=True)[0:int(len(ranks) * percentage)][-1]

        short_summary = list()
        for sentence in self.sentences:
            if sentence.rank > threshold:
                short_summary.append(sentence)
        return short_summary


