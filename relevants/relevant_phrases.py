import uuid
import math
import sys

import pytextrank

def generate_id():
    return uuid.uuid4()

class RelevantPhrases(object):
    def __init__(self, stopwords=None):
        self.stopwords = self.load_stopwords(stopwords)
        self.groups_text = {}
        self.groups_phrases = {}

    def add_text(self, text, group_id=None):
        group_id = self.get_group(group_id)
        if self.groups_text.get(group_id) is None:
            self.groups_text[group_id] = []
        self.groups_text[group_id].append({"id": generate_id(), "text": text})

    @staticmethod
    def load_stopwords(stopwords_path):
        if stopwords_path is None:
            return dict()
        return dict(
            [
                (stopword.strip("\r\n"), 1)
                for stopword in open(stopwords_path).readlines()
            ]
        )

    @staticmethod
    def get_group(group_id):
        if group_id is None:
            group_id = "__default"
        return group_id

    def generate_graph(self, group_id=None):
        """Generates a text graph for each sentence"""
        group_id = self.get_group(group_id)
        graphs = []
        for graf in pytextrank.parse_doc(self.groups_text[group_id]):
            graphs.append(graf._asdict())
        return graphs

    def generate_phrases(self, group_id, graphs):
        """From the graph, take the phrases, with their count, rank"""
        _, ranks = pytextrank.text_rank(graphs)
        if self.groups_phrases.get(group_id) is None:
            self.groups_phrases[group_id] = []
        for normal_phrase in pytextrank.normalize_key_phrases(
                graphs, ranks, stopwords=["not_a_word______",]
                # Setting that stopword is needed, because we dont want
                # that pytextrank, remove stopwords at this point.
            ):
            self.groups_phrases[group_id].append(dict(normal_phrase._asdict()))

    def calculate(self, group_id=None):
        group_id = self.get_group(group_id)
        graphs = self.generate_graph(group_id)
        self.generate_phrases(group_id, graphs)
        phrases_no_stop_words = []
        for phrase in self.groups_phrases[group_id]:
            if not self.stopwords or self.stopwords.get(phrase.get("text")) is None:
                phrases_no_stop_words.append(phrase)
        if self.groups_phrases.get(group_id) is None:
            self.groups_phrases[group_id] = []
        self.groups_phrases[group_id] = phrases_no_stop_words

class Stopwords(object):
    def __init__(self, relevant_phrases, min_count=2):
        self.relevant_phrases = relevant_phrases
        self.idf = {}
        self.tfidf = {}
        self.possible_stopwords = {}
        self.groups_count = len(relevant_phrases.groups_phrases.keys())
        self.groups_phrases = {}
        for group_id in relevant_phrases.groups_phrases.keys():
            phrases = []
            for phrase_data in relevant_phrases.groups_phrases[group_id]:
                if phrase_data.get("count") >= min_count:
                    phrases.append(phrase_data)
            self.groups_phrases[group_id] = phrases
        self.groups_words_counts = dict([
            (
                group_id,
                sum([
                    phrase_data.get("count") or 0
                    for phrase_data in self.groups_phrases[group_id]
                ])
            )
            for group_id in self.groups_phrases
        ])
    def _get_phrase_data(self, group_id, word):
        return ([
            phrase_data
            for phrase_data in self.groups_phrases[group_id]
            if phrase_data.get("text") == word
        ] or [None,])[0]


    def get_tf(self, group_id, phrase_data):
        words_count_in_group = phrase_data["count"] or 0
        return words_count_in_group / self.groups_words_counts[group_id]

    def get_idf(self, phrase_data):
        if self.idf.get(phrase_data["text"]) is None:
            self.idf[phrase_data["text"]] = math.log(
                1.0 * self.groups_count / (
                    1 + len([
                        1 for group_id in self.groups_phrases
                        if self._get_phrase_data(group_id, phrase_data["text"])
                    ])
                )
            )
        return self.idf[phrase_data["text"]]

    @staticmethod
    def _group_possible_stopwords(possible_swords_by_group):
        group_possible_stopwords = {}
        for group_id in possible_swords_by_group.keys():
            for position, possible_stopword_data in enumerate(possible_swords_by_group[group_id]):
                possible_stopword_text = possible_stopword_data[0]
                if group_possible_stopwords.get(possible_stopword_text) is None:
                    group_possible_stopwords[possible_stopword_text] = []
                group_possible_stopwords[possible_stopword_text].append(position)
        possible_stopwords = []
        print("total words", len(group_possible_stopwords.keys()), file=sys.stderr)
        for phrase, positions in group_possible_stopwords.items():
            possible_stopwords.append(
                (phrase, sum(positions)/len(positions))
            )
        return [
            posible_stopword_data[0]
            for posible_stopword_data in sorted(possible_stopwords, key=lambda x: x[1])
        ]

    def calculate_stopwords(self):
        phrases = []
        possible_swords_by_group = {}
        for group_id in self.relevant_phrases.groups_phrases.keys():
            print("stopwords_calculate: %s" % group_id, file=sys.stderr)
            for phrase_data in self.relevant_phrases.groups_phrases[group_id]:
                tfidf = self.get_tf(group_id, phrase_data) * self.get_idf(phrase_data)
                phrases.append(
                    (
                        phrase_data.get("text"),
                        tfidf
                    )
                )
            possible_swords_by_group[group_id] = sorted(phrases, key=lambda x: x[1])
        return self._group_possible_stopwords(possible_swords_by_group)
