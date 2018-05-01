import sys
import gzip
import glob
import os
from random import randint

from relevant_phrases import RelevantPhrases, Stopwords, Phrases

def print_row(row):
    print("\t".join([str(el) for el in row]))

def read_rows(input_path, sep="\t"):
    if input_path.find(".gz") > 0:
        input_file = gzip.open(input_path, 'rt')
    else:
        input_file = open(input_path, 'rt')

    for line in input_file:
        yield line.rstrip("\r\n").split(sep)

def prepare_text(rows, column_index):
    id_ = randint(1, 10000000000)
    text = "\n".join([row[column_index] for row in rows])
    return [{"id": id_, "text": text}, ]

def calculate_textrank_for_folder(folder_path, column_index, stopwords=None):
    text_rank = RelevantPhrases(stopwords)
    group_id = None
    for input_path in glob.glob(folder_path + "/*.tsv"):
        group_id = os.path.basename(input_path).replace(".tsv", "")
        print(group_id, file=sys.stderr)
        rows = read_rows(input_path, sep="\t")
        for row in rows:
            text_rank.add_text(row[column_index], group_id)
        text_rank.calculate(group_id)
    return text_rank

def main():
    folder_path = sys.argv[2]
    column_index = int(sys.argv[3]) - 1

    relevant_phrases = calculate_textrank_for_folder(
        folder_path, column_index, stopwords="data/stopwords.txt"
    )
    print_row(["group_id", "phrase", "count", "rank"])
    for group_id in relevant_phrases.groups_phrases:
        for phrase_data in sorted(
                relevant_phrases.groups_phrases[group_id],
                key=lambda x: x.get("count") * x.get("rank"),
                reverse=True
            ):
            print_row(
                [
                    group_id,
                    phrase_data.get("text"),
                    phrase_data.get("count"),
                    phrase_data.get("rank")
                ]
            )

def calculate_stopwords():
    folder_path = sys.argv[2]
    column_index = int(sys.argv[3]) - 1

    phrases = []
    for input_path in glob.glob(folder_path + "/*.tsv"):
        file_id = input_path.split("/")[-1].split(".tsv")[0]
        for row in read_rows(input_path, sep="\t"):
            phrases.append((file_id, Phrases([row[column_index], ]).all_phrases))
    stop_words_instance = Stopwords(phrases)
    stopwords = stop_words_instance.calculate_stopwords()
    for stopword in stopwords:
        print(stopword)

if __name__ == "__main__":
    if sys.argv[1] == "relevants":
        main()
    elif sys.argv[1] == "stopwords":
        calculate_stopwords()
