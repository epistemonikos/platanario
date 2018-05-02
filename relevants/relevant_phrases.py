import uuid
import math
import sys

import pytextrank

def generate_id():
    return uuid.uuid4()

class Phrases(object):
    def __init__(self, texts):
        self.texts = texts
        self.graphs = self.generate_graph()
        self.all_phrases = []
        self.generate_phrases()

    def generate_graph(self):
        """Generates a text graph for each sentence"""
        graphs = []
        for graf in pytextrank.parse_doc([
                {"id": generate_id(), "text": text}
                for text in self.texts
        ]):
            graphs.append(graf._asdict())
        return graphs

    def generate_phrases(self):
        """From the graph, take the phrases, with their count, rank"""
        _, ranks = pytextrank.text_rank(self.graphs)
        for normal_phrase in pytextrank.normalize_key_phrases(
                self.graphs, ranks, stopwords=["not_a_word______",]
                # Setting that stopword is needed, because we dont want
                # that pytextrank, remove stopwords at this point.
            ):
            self.all_phrases.append(dict(normal_phrase._asdict()))

class RelevantPhrases(object):
    def __init__(self, stopwords=None):
        self.stopwords = self.load_stopwords(stopwords)
        self.groups_text = {}
        self.groups_phrases = {}

    def add_text(self, text, group_id=None):
        group_id = self.get_group(group_id)
        if self.groups_text.get(group_id) is None:
            self.groups_text[group_id] = []
        self.groups_text[group_id].append(text)

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

    def calculate(self, group_id=None):
        group_id = self.get_group(group_id)
        phrases = Phrases(self.groups_text[group_id])
        phrases_no_stop_words = []
        for phrase in phrases.all_phrases:
            if not self.stopwords or self.stopwords.get(phrase.get("text")) is None:
                phrases_no_stop_words.append(phrase)
        if self.groups_phrases.get(group_id) is None:
            self.groups_phrases[group_id] = []
        self.groups_phrases[group_id] = phrases_no_stop_words

class Stopwords(object):
    def __init__(self, documents_phrases, min_count=2):
        self.idf = {}
        self.tfidf = {}
        self.possible_stopwords = {}
        self.documents_phrases = documents_phrases
        self.documents_count = len(documents_phrases)
        self.phrases_in_documents = {}
        self.phrases_in_groups = {}
        for group_id, document_phrases in self.documents_phrases:
            for phrase_data in document_phrases:
                if not self.phrases_in_documents.get(phrase_data['text']):
                    self.phrases_in_documents[phrase_data['text']] = 0
                self.phrases_in_documents[phrase_data['text']] += 1
                if not self.phrases_in_groups.get(phrase_data['text']):
                    self.phrases_in_groups[phrase_data['text']] = []
                if group_id not in self.phrases_in_groups[phrase_data['text']]:
                    self.phrases_in_groups[phrase_data['text']].append(group_id)

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
                (phrase, sum(positions)/len(positions), len(positions))
            )
        return [
            posible_stopword_data[0]
            for posible_stopword_data in sorted(possible_stopwords, key=lambda x: x[1])
        ]

    def calculate_stopwords(self):
        phrases = {}
        possible_swords_by_group = {}
        for group_id, group_phrases in self.documents_phrases:
            for phrase_data in group_phrases:
                phrase_text = phrase_data['text']
                if not phrases.get(phrase_text):
                    score = (
                        1.0 / self.phrases_in_documents[phrase_text]
                    ) / len(self.phrases_in_groups[phrase_text])
                    phrases[phrase_text] = score
            possible_swords_by_group[group_id] = sorted(phrases.items(), key=lambda x: x[1])
        return self._group_possible_stopwords(possible_swords_by_group)
