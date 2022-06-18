import os.path
import sys
from parser import token_sent
import ModelSummary
from highlight import highlight_phrases

def load(fp):
    data = fp.read()

    sent_tokens = token_sent(data)
    return ModelSummary.Model_Summary(sent_tokens)

def main():
    filename = "./rinput.txt"
    num_of_sentences = 200
    output_file = "result"

    if not (os.path.isfile(filename)):
        print("File not Found")
        sys.exit(1)

    fp = open(filename, 'r')

    model = load(fp)
    fp.close()

    model.compress_sentences()

    model.rank_sentences()
    model.rake_sentences()

    short_summary = model.top_sent(num_of_sentences)
    print(f"{num_of_sentences} lines of the Summary")
    
    
    for i,sentence in enumerate(short_summary):
        print(i,sentence.sentence)
    nfile = output_file + ".txt"
    with open(nfile, 'w') as f:
        f.write('\n'.join([s.sentence for s in short_summary]))
        f.write("\n")
    
    html_output = highlight_phrases(model.sentences)

    f_name = output_file+".html"
    fd = open(f_name, "w")
    fd.write(html_output)

main()