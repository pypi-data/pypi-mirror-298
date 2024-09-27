from .mainClass import *

from typing import List, Dict

class Levenshtein(Distance):
	
	def __init__(self):
		super().__init__()
		
	def compute(self,s1: str, s2: str) -> int:
		
		dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

		for i in range(len(s1) + 1):
			dp[i][0] = i
		for j in range(len(s2) + 1):
			dp[0][j] = j

		for i in range(1, len(s1) + 1):
			for j in range(1, len(s2) + 1):
				if s1[i - 1] == s2[j - 1]:
					cost = 0
				else:
					cost = 1
				dp[i][j] = min(dp[i - 1][j] + 1,        # Suppression
                           dp[i][j - 1] + 1,        # Insertion
                           dp[i - 1][j - 1] + cost) # Substitution

		return dp[len(s1)][len(s2)]
		
	def exemple(self):
		self.obj1_exemple = "kitten"
		self.obj2_exemple = "sitting"
		super().exemple()

class DamerauLevenshtein(Distance):
	
	def __init__(self):
		super().__init__()
		
	def compute(self,s1 :str, s2 :str) -> int:
		d = {}
		lenstr1 = len(s1)
		lenstr2 = len(s2)

		for i in range(-1, lenstr1 + 1):
			d[(i, -1)] = i + 1
		for j in range(-1, lenstr2 + 1):
			d[(-1, j)] = j + 1

		for i in range(lenstr1):
			for j in range(lenstr2):
				cost = 0 if s1[i] == s2[j] else 1
				d[(i, j)] = min(
					d[(i - 1, j)] + 1,  # suppresion
					d[(i, j - 1)] + 1,  # insertion
					d[(i - 1, j - 1)] + cost,  # substitution
				)
				if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
					d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)  # transposition

		return d[lenstr1 - 1, lenstr2 - 1]
		
	def exemple(self):
		self.obj1_exemple = "ca"
		self.obj2_exemple = "abc"

		super().exemple()

class Hamming(Distance):
	
	def __init__(self):
		super().__init__()
		
	def compute(self,str1: str, str2: str) -> int:
		"""
		Calculate the Hamming distance between two strings.
    
		:param str1: First string
		:param str2: Second string
		:return: Hamming distance between str1 and str2
		:raises ValueError: If the strings are not of the same length
		"""
		return sum(el1 != el2 for el1, el2 in zip(str1, str2))
		
	def exemple(self):
		self.obj1_exemple = "1011101"
		self.obj2_exemple = "1001001"
		super().exemple()

class Cosine(Distance):
	
	def __init__(self):
		super().__init__()

	def compute(self,vec1 :list, vec2 :list) -> float:
		"""
		Calculate the cosine similarity between two vectors.
    
		:param vec1: First vector
		:param vec2: Second vector
		:return: Cosine similarity between vec1 and vec2
		"""
		dot_prod = Vector.dot_product(vec1, vec2)
		norm_vec1 = Vector().norm(vec1)
		norm_vec2 = Vector().norm(vec2)
		if norm_vec1 == 0 or norm_vec2 == 0:
			# Handling edge case if any vector has zero length to avoid division by zero
			return 0.0
		return dot_prod / (norm_vec1 * norm_vec2)

import math
from typing import List, Dict
from collections import Counter

class TFIDFDistance:
    def __init__(self, corpus: List[str]) -> None:
        """
        Initialisation de la classe TFIDFDistance.
        
        :param corpus: Liste de documents (chaîne de caractères) utilisés pour calculer les fréquences globales des termes.
        """
        self.corpus = corpus
        self.term_frequencies = self._compute_term_frequencies(corpus)
        self.document_frequencies = self._compute_document_frequencies(corpus)

    def _compute_term_frequencies(self, corpus: List[str]) -> List[Dict[str, int]]:
        """
        Calcule la fréquence des termes pour chaque document du corpus.
        
        :param corpus: Liste de documents.
        :return: Liste de dictionnaires de fréquences de termes pour chaque document.
        """
        term_frequencies = [Counter(doc.split()) for doc in corpus]
        return term_frequencies

    def _compute_document_frequencies(self, corpus: List[str]) -> Dict[str, int]:
        """
        Calcule la fréquence inverse des documents (DF) pour chaque terme du corpus.
        
        :param corpus: Liste de documents.
        :return: Dictionnaire de fréquence inverse des documents pour chaque terme.
        """
        doc_freq: Dict[str, int] = {}
        for document in corpus:
            unique_terms = set(document.split())
            for term in unique_terms:
                doc_freq[term] = doc_freq.get(term, 0) + 1
        return doc_freq

    def _compute_tf_idf(self, document: str) -> Dict[str, float]:
        """
        Calcule les valeurs TF-IDF pour un document donné.
        
        :param document: Chaîne de caractères représentant un document.
        :return: Dictionnaire des valeurs TF-IDF pour chaque terme du document.
        """
        term_freq: Dict[str, int] = Counter(document.split())
        total_terms = len(document.split())
        tf_idf: Dict[str, float] = {}
        
        for term, freq in term_freq.items():
            tf = freq / total_terms
            idf = math.log(len(self.corpus) / (1 + self.document_frequencies.get(term, 0)))
            tf_idf[term] = tf * idf

        return tf_idf

    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Calcule la similarité cosinus entre deux vecteurs TF-IDF.
        
        :param vec1: Premier vecteur TF-IDF.
        :param vec2: Deuxième vecteur TF-IDF.
        :return: Valeur de similarité cosinus.
        """
        intersection = set(vec1.keys()).intersection(vec2.keys())
        dot_product = sum(vec1[term] * vec2[term] for term in intersection)
        
        norm1 = math.sqrt(sum([value ** 2 for value in vec1.values()]))
        norm2 = math.sqrt(sum([value ** 2 for value in vec2.values()]))
        
        if not norm1 or not norm2:
            return 0.0
        
        return dot_product / (norm1 * norm2)

    def compare(self, text1: str, text2: str) -> float:
        """
        Compare deux textes en utilisant la distance TF-IDF (Cosine Similarity).
        
        :param text1: Premier document à comparer.
        :param text2: Deuxième document à comparer.
        :return: Valeur de la similarité entre 0 et 1 (plus elle est proche de 1, plus les documents sont similaires).
        """
        tf_idf1 = self._compute_tf_idf(text1)
        tf_idf2 = self._compute_tf_idf(text2)
        return self._cosine_similarity(tf_idf1, tf_idf2)

# Exemple d'utilisation
corpus = [
    "the cat sat on the mat",
    "the dog sat on the mat",
    "the dog chased the cat"
]

text1 = "the cat is sitting on the mat"
text2 = "the dog is sitting on the mat"

tfidf_distance = TFIDFDistance(corpus)
similarity_score: float = tfidf_distance.compare(text1, text2)

print(f"TF-IDF Similarity: {similarity_score}")

class SimHash:
    """
    A class to compute the SimHash of a document and to compare the SimHash values of two documents
    to measure their similarity.
    """

    def _hash(self, token: str) -> int:
        """
        Converts a token (string) into a 64-bit integer hash.

        :param token: The input string (token) to be hashed.
        :return: A 64-bit integer hash of the input token.
        """
        return int.from_bytes(token.encode('utf-8'), 'little') % (1 << 64)

    def _tokenize(self, document: str) -> List[str]:
        """
        Tokenizes the document into individual words (or tokens).

        :param document: The input document as a string.
        :return: A list of tokens (words) from the document.
        """
        return document.split()

    def _compute_weights(self, tokens: List[str]) -> Dict[str, int]:
        """
        Computes the weight of each token based on its frequency in the document.

        :param tokens: A list of tokens extracted from the document.
        :return: A dictionary where keys are tokens and values are their frequencies (weights).
        """
        token_weights: Dict[str, int] = {}
        for token in tokens:
            if token in token_weights:
                token_weights[token] += 1
            else:
                token_weights[token] = 1
        return token_weights

    def _compute_simhash(self, token_weights: Dict[str, int]) -> int:
        """
        Computes the SimHash value from the token weights using a weighted hash for each token.

        :param token_weights: A dictionary of token weights.
        :return: A 64-bit integer representing the SimHash value.
        """
        bit_vector: List[int] = [0] * 64

        for token, weight in token_weights.items():
            token_hash: int = self._hash(token)

            for i in range(64):
                # Extract each bit from the 64-bit hash
                bit = (token_hash >> i) & 1
                # Adjust the bit vector based on the weight
                if bit == 1:
                    bit_vector[i] += weight
                else:
                    bit_vector[i] -= weight

        # Convert bit_vector into a 64-bit SimHash
        simhash_value: int = 0
        for i in range(64):
            if bit_vector[i] > 0:
                simhash_value |= (1 << i)

        return simhash_value

    def compute(self, document: str) -> int:
        """
        Computes the SimHash value of a given document.

        :param document: The input document as a string.
        :return: A 64-bit integer representing the SimHash value.
        """
        tokens: List[str] = self._tokenize(document)
        token_weights: Dict[str, int] = self._compute_weights(tokens)
        simhash_value: int = self._compute_simhash(token_weights)
        return simhash_value

    def hamming_distance(self, hash1: int, hash2: int) -> int:
        """
        Computes the Hamming distance between two 64-bit SimHash values.

        :param hash1: The first SimHash value.
        :param hash2: The second SimHash value.
        :return: The Hamming distance between the two SimHash values.
        """
        x: int = hash1 ^ hash2
        distance: int = 0
        while x:
            distance += x & 1
            x >>= 1
        return distance

    def similarity(self, document1: str, document2: str) -> float:
        """
        Computes the similarity between two documents based on their SimHash values.

        :param document1: The first document as a string.
        :param document2: The second document as a string.
        :return: A similarity score between 0 (completely different) and 1 (identical).
        """
        simhash1: int = self.compute(document1)
        simhash2: int = self.compute(document2)

        # Calculate Hamming distance
        hamming_dist: int = self.hamming_distance(simhash1, simhash2)
        max_bits: int = 64

        # Compute similarity as the fraction of matching bits
        similarity_score: float = (max_bits - hamming_dist) / max_bits
        return similarity_score


# Example usage:
if __name__ == "__main__":
    simhash = SimHash()

    # Two example documents
    doc1: str = "This is a sample document."
    doc2: str = "This is another sample document."

    # Compute similarity between the two documents
    similarity_score: float = simhash.similarity(doc1, doc2)

    # Print similarity score (0 means completely different, 1 means identical)
    print(f"Similarity score between documents: {similarity_score}")

from typing import List, Dict
import math


class CosineSimilarity:
    """
    A class to compute the Cosine Similarity between two text documents based on term frequency vectors.
    """

    def _tokenize(self, document: str) -> List[str]:
        """
        Tokenizes the document into individual words (tokens).
        
        :param document: The input document as a string.
        :return: A list of tokens (words) from the document.
        """
        return document.lower().split()

    def _compute_term_frequencies(self, tokens: List[str]) -> Dict[str, int]:
        """
        Computes the term frequency (TF) of each token in the document.
        
        :param tokens: A list of tokens extracted from the document.
        :return: A dictionary where keys are tokens and values are their frequencies in the document.
        """
        term_frequencies: Dict[str, int] = {}
        for token in tokens:
            if token in term_frequencies:
                term_frequencies[token] += 1
            else:
                term_frequencies[token] = 1
        return term_frequencies

    def _dot_product(self, vec1: Dict[str, int], vec2: Dict[str, int]) -> float:
        """
        Computes the dot product of two term frequency vectors.
        
        :param vec1: The first term frequency vector as a dictionary.
        :param vec2: The second term frequency vector as a dictionary.
        :return: The dot product of the two vectors.
        """
        dot_product: float = 0.0
        for term, freq in vec1.items():
            if term in vec2:
                dot_product += freq * vec2[term]
        return dot_product

    def _magnitude(self, vec: Dict[str, int]) -> float:
        """
        Computes the magnitude (Euclidean norm) of a term frequency vector.
        
        :param vec: A term frequency vector as a dictionary.
        :return: The magnitude of the vector.
        """
        magnitude: float = math.sqrt(sum(freq ** 2 for freq in vec.values()))
        return magnitude

    def compute(self, document1: str, document2: str) -> float:
        """
        Computes the Cosine Similarity between two documents.
        
        :param document1: The first document as a string.
        :param document2: The second document as a string.
        :return: The cosine similarity score between 0 and 1.
        """
        # Tokenize both documents
        tokens1: List[str] = self._tokenize(document1)
        tokens2: List[str] = self._tokenize(document2)

        # Compute term frequencies
        tf1: Dict[str, int] = self._compute_term_frequencies(tokens1)
        tf2: Dict[str, int] = self._compute_term_frequencies(tokens2)

        # Compute the dot product of the two vectors
        dot_product: float = self._dot_product(tf1, tf2)

        # Compute the magnitude of each vector
        magnitude1: float = self._magnitude(tf1)
        magnitude2: float = self._magnitude(tf2)

        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        # Compute and return the cosine similarity
        cosine_similarity: float = dot_product / (magnitude1 * magnitude2)
        return cosine_similarity


# Example usage:
if __name__ == "__main__":
    cosine_similarity = CosineSimilarity()

    # Two example documents
    doc1: str = "This is a sample document."
    doc2: str = "This is another sample document."

    # Compute cosine similarity between the two documents
    similarity_score: float = cosine_similarity.compute(doc1, doc2)

    # Print similarity score (0 means no similarity, 1 means identical)
    print(f"Cosine Similarity score between documents: {similarity_score}")

from typing import List, Dict, Set, Tuple
import math


class TFIDFSimilarity:
    """
    A class to compute the similarity between two documents based on TF-IDF (Term Frequency-Inverse Document Frequency).
    """

    def _tokenize(self, document: str) -> List[str]:
        """
        Tokenizes the document into individual words (tokens).
        
        :param document: The input document as a string.
        :return: A list of tokens (words) from the document.
        """
        return document.lower().split()

    def _compute_term_frequencies(self, tokens: List[str]) -> Dict[str, int]:
        """
        Computes the term frequency (TF) of each token in the document.
        
        :param tokens: A list of tokens extracted from the document.
        :return: A dictionary where keys are tokens and values are their frequencies in the document.
        """
        term_frequencies: Dict[str, int] = {}
        for token in tokens:
            if token in term_frequencies:
                term_frequencies[token] += 1
            else:
                term_frequencies[token] = 1
        return term_frequencies

    def _compute_document_frequencies(self, documents: List[List[str]]) -> Dict[str, int]:
        """
        Computes the document frequency (DF) for each token across multiple documents.
        
        :param documents: A list of tokenized documents (each document is a list of tokens).
        :return: A dictionary where keys are tokens and values are the number of documents containing the token.
        """
        document_frequencies: Dict[str, int] = {}
        for tokens in documents:
            unique_tokens: Set[str] = set(tokens)
            for token in unique_tokens:
                if token in document_frequencies:
                    document_frequencies[token] += 1
                else:
                    document_frequencies[token] = 1
        return document_frequencies

    def _compute_tfidf(self, term_freq: Dict[str, int], doc_freq: Dict[str, int], total_docs: int) -> Dict[str, float]:
        """
        Computes the TF-IDF value for each token in the document.
        
        :param term_freq: Term frequency for a document.
        :param doc_freq: Document frequency for all documents.
        :param total_docs: Total number of documents.
        :return: A dictionary where keys are tokens and values are their TF-IDF values.
        """
        tfidf: Dict[str, float] = {}
        for term, freq in term_freq.items():
            tf: float = freq / sum(term_freq.values())
            idf: float = math.log(total_docs / (1 + doc_freq.get(term, 0)))
            tfidf[term] = tf * idf
        return tfidf

    def _dot_product(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Computes the dot product of two TF-IDF vectors.
        
        :param vec1: The first TF-IDF vector as a dictionary.
        :param vec2: The second TF-IDF vector as a dictionary.
        :return: The dot product of the two vectors.
        """
        dot_product: float = 0.0
        for term, value in vec1.items():
            if term in vec2:
                dot_product += value * vec2[term]
        return dot_product

    def _magnitude(self, vec: Dict[str, float]) -> float:
        """
        Computes the magnitude (Euclidean norm) of a TF-IDF vector.
        
        :param vec: A TF-IDF vector as a dictionary.
        :return: The magnitude of the vector.
        """
        magnitude: float = math.sqrt(sum(value ** 2 for value in vec.values()))
        return magnitude

    def compute(self, document1: str, document2: str, corpus: List[str]) -> float:
        """
        Computes the TF-IDF similarity (cosine similarity) between two documents based on a corpus of documents.
        
        :param document1: The first document as a string.
        :param document2: The second document as a string.
        :param corpus: A list of documents representing the corpus.
        :return: The TF-IDF similarity score between 0 and 1.
        """
        # Tokenize both documents and the corpus
        tokens1: List[str] = self._tokenize(document1)
        tokens2: List[str] = self._tokenize(document2)
        tokenized_corpus: List[List[str]] = [self._tokenize(doc) for doc in corpus]

        # Add the documents to the corpus for frequency calculations
        tokenized_corpus.append(tokens1)
        tokenized_corpus.append(tokens2)

        # Compute term frequencies for both documents
        tf1: Dict[str, int] = self._compute_term_frequencies(tokens1)
        tf2: Dict[str, int] = self._compute_term_frequencies(tokens2)

        # Compute document frequencies from the corpus
        doc_freq: Dict[str, int] = self._compute_document_frequencies(tokenized_corpus)

        # Total number of documents
        total_docs: int = len(tokenized_corpus)

        # Compute TF-IDF vectors for both documents
        tfidf1: Dict[str, float] = self._compute_tfidf(tf1, doc_freq, total_docs)
        tfidf2: Dict[str, float] = self._compute_tfidf(tf2, doc_freq, total_docs)

        # Compute the dot product of the two TF-IDF vectors
        dot_product: float = self._dot_product(tfidf1, tfidf2)

        # Compute the magnitude of each TF-IDF vector
        magnitude1: float = self._magnitude(tfidf1)
        magnitude2: float = self._magnitude(tfidf2)

        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        # Compute and return the TF-IDF cosine similarity
        tfidf_similarity: float = dot_product / (magnitude1 * magnitude2)
        return tfidf_similarity


# Example usage:
if __name__ == "__main__":
    tfidf_similarity = TFIDFSimilarity()

    # Two example documents
    doc1: str = "This is a sample document."
    doc2: str = "This document is a simple example."

    # Corpus of documents for TF-IDF calculations
    corpus: List[str] = [
        "This is a document in the corpus.",
        "Another document is here for testing.",
        "This example is part of the corpus."
    ]

    # Compute TF-IDF similarity between the two documents
    similarity_score: float = tfidf_similarity.compute(doc1, doc2, corpus)

    # Print similarity score (0 means no similarity, 1 means identical)
    print(f"TF-IDF Similarity score between documents: {similarity_score}")

from typing import List


class LongestCommonSubsequence:
    """
    A class to compute the Longest Common Subsequence (LCS) between two text files.
    """

    def _lcs_matrix(self, text1: str, text2: str) -> List[List[int]]:
        """
        Constructs the LCS matrix for two input texts.
        
        :param text1: The first text as a string.
        :param text2: The second text as a string.
        :return: A 2D list (matrix) containing the lengths of LCS for substrings of text1 and text2.
        """
        len1: int = len(text1)
        len2: int = len(text2)
        
        # Create a 2D matrix initialized with 0
        lcs_matrix: List[List[int]] = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                if text1[i - 1] == text2[j - 1]:
                    lcs_matrix[i][j] = lcs_matrix[i - 1][j - 1] + 1
                else:
                    lcs_matrix[i][j] = max(lcs_matrix[i - 1][j], lcs_matrix[i][j - 1])

        return lcs_matrix

    def _backtrack_lcs(self, lcs_matrix: List[List[int]], text1: str, text2: str) -> str:
        """
        Backtracks through the LCS matrix to reconstruct the longest common subsequence.
        
        :param lcs_matrix: A 2D list (matrix) containing the lengths of LCS for substrings of text1 and text2.
        :param text1: The first text as a string.
        :param text2: The second text as a string.
        :return: The longest common subsequence as a string.
        """
        i: int = len(text1)
        j: int = len(text2)
        lcs: List[str] = []

        while i > 0 and j > 0:
            if text1[i - 1] == text2[j - 1]:
                lcs.append(text1[i - 1])
                i -= 1
                j -= 1
            elif lcs_matrix[i - 1][j] >= lcs_matrix[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return ''.join(reversed(lcs))

    def compute(self, text1: str, text2: str) -> str:
        """
        Computes the Longest Common Subsequence (LCS) between two texts.
        
        :param text1: The first text as a string.
        :param text2: The second text as a string.
        :return: The longest common subsequence as a string.
        """
        # Compute the LCS matrix
        lcs_matrix: List[List[int]] = self._lcs_matrix(text1, text2)

        # Backtrack to find the actual LCS
        lcs: str = self._backtrack_lcs(lcs_matrix, text1, text2)

        return lcs


# Example usage:
if __name__ == "__main__":
    lcs_calculator = LongestCommonSubsequence()

    # Two example text inputs
    text1: str = "AGGTAB"
    text2: str = "GXTXAYB"

    # Compute the LCS
    lcs_result: str = lcs_calculator.compute(text1, text2)

    # Print the LCS
    print(f"The Longest Common Subsequence is: {lcs_result}")


from typing import List, Optional
#from gensim.models import KeyedVectors
#from gensim.similarities import WmdSimilarity
#from gensim.corpora.dictionary import Dictionary

import gensim.downloader as api

# Import and download stopwords from NLTK.
from nltk.corpus import stopwords
from nltk import download

class WordMoversDistance:
    def __init__(self) -> None:
        """
        Initialize the WordMoversDistance class with a pre-trained word embedding model and a corpus of texts.

        :param model: A pre-trained word embedding model (e.g., Word2Vec or GloVe).
        :param texts: A list of text documents to be compared.
        """
        
        download('stopwords')  # Download stopwords list.
        self.stop_words = stopwords.words('english')
        self.model = api.load('word2vec-google-news-300')
        #or download -> https://www.kaggle.com/datasets/leadbest/googlenewsvectorsnegative300?resource=download


    def preprocess(self,sentence):
        return [w for w in sentence.lower().split() if w not in self.stop_words]
        

    def compute_distance(self, text1: str, text2: str) -> Optional[float]:
        """
        Compute the Word Mover's Distance between two text documents.

        :param text1: The first text document.
        :param text2: The second text document.
        :return: The Word Mover's Distance between the two documents, or None if it cannot be computed.
        """
        tokens1: List[str] = self.preprocess(text1)
        tokens2: List[str] = self.preprocess(text2)
                
        if tokens1 and tokens2:
            return self.model.wmdistance(tokens1, tokens2)
        return None

    def compute(self,text1: str, text2: str) -> Optional[float]:
        """
        Compare two text files using Word Mover's Distance and a pre-trained word embedding model.

        :param text1: first text.
        :param text2: second text.
        :return: The Word Mover's Distance between the two text files, or None if it cannot be computed.
        """
        try:
            # Load the pre-trained word embedding model
            #model: KeyedVectors = KeyedVectors.load_word2vec_format(model_path, binary=True)

            # Compute and return the Word Mover's Distance
            return self.model.wmdistance(text1, text2)

        except Exception as e:
            print(f"Error processing files: {e}")
            return None


if __name__ == "__main__":
    # Example usage comparing two text 
    
    str1: str= 'Obama speaks to the media in Illinois'
    str2: str = 'The president greets the press in Chicago'
    
    wmd_distance: Optional[float] = WordMoversDistance().compute(str1, str2)
    

    if wmd_distance is not None:
        print(f"Word Mover's Distance between files: {wmd_distance}")
    else:
        print("Could not compute Word Mover's Distance.")

from typing import List, Optional
from transformers import BertTokenizer, BertModel
import torch

class BERTBasedDistance:
    def __init__(self, model_name: str = "bert-base-uncased") -> None:
        """
        Initialize the BERTBasedDistance class with a BERT model and tokenizer.

        :param model_name: The name of the pre-trained BERT model to use.
        """
        self.tokenizer: BertTokenizer = BertTokenizer.from_pretrained(model_name)
        self.model: BertModel = BertModel.from_pretrained(model_name)

    def _encode_text(self, text: str) -> torch.Tensor:
        """
        Encode a text into a BERT embedding.

        :param text: The input text to encode.
        :return: A tensor representing the embedding of the input text.
        """
        inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)  # Mean pooling over the sequence length

    def compute_distance(self, text1: str, text2: str) -> float:
        """
        Compute the cosine similarity between the BERT embeddings of two texts.

        :param text1: The first text document.
        :param text2: The second text document.
        :return: The cosine similarity between the embeddings of the two documents.
        """
        embedding1: torch.Tensor = self._encode_text(text1)
        embedding2: torch.Tensor = self._encode_text(text2)

        # Cosine similarity between the two embeddings
        similarity: float = torch.nn.functional.cosine_similarity(embedding1, embedding2).item()
        return similarity

    @staticmethod
    def compute(text1: str, text2: str) -> Optional[float]:
        """
        Compare two text files using BERT embeddings to calculate semantic similarity.

        :param file1_path: Path to the first text file.
        :param file2_path: Path to the second text file.
        :return: The similarity score between the two text files based on BERT embeddings.
        """
        try:

            # Initialize BERTBasedDistance object
            bert_distance = BERTBasedDistance()

            # Compute and return the similarity score
            return bert_distance.compute_distance(text1, text2)

        except Exception as e:
            print(f"Error processing files: {e}")
            return None


if __name__ == "__main__":
    # Example usage comparing two text files
    str1: str= 'Obama speaks to the media in Illinois'
    str2: str = 'The president greets the press in Chicago'

    similarity_score: Optional[float] = BERTBasedDistance.compute(str1, str2)

    if similarity_score is not None:
        print(f"BERT-based similarity between files: {similarity_score}")
    else:
        print("Could not compute BERT-based similarity.")

class JaroWinkler(Distance):
	
	def __init__(self):
		super().__init__()

	def compute(self,s1 :str, s2 :str, p=0.1) -> float:
		"""
		Calculate the Jaro-Winkler distance between two strings.
    
		:param s1: The first string
		:param s2: The second string
		:param p: The scaling factor, usually 0.1
		:return: Jaro-Winkler distance between the two strings
		"""
		jaro_sim = Jaro().calculate(s1, s2)

		prefix_length = 0
		max_prefix_length = 4

		for i in range(min(len(s1), len(s2))):
			if s1[i] == s2[i]:
				prefix_length += 1
			else:
				break
			if prefix_length == max_prefix_length:
				break

		jaro_winkler_sim = jaro_sim + (prefix_length * p * (1 - jaro_sim))
		return jaro_winkler_sim
		
	def exemple(self):
		self.obj1_exemple = "martha"
		self.obj2_exemple = "marhta"
		super().exemple()

from typing import Set

class OverlapCoefficient:
    def __init__(self) -> None:
        """
        Initialisation de la classe OverlapCoefficient.
        """
        pass

    def compute(self, set1: Set[str], set2: Set[str]) -> float:
        """
        Calcule le coefficient de chevauchement (Overlap Coefficient) entre deux ensembles de mots.
        
        :param set1: Premier ensemble de mots.
        :param set2: Deuxième ensemble de mots.
        :return: Coefficient de chevauchement entre les deux ensembles, entre 0 et 1.
        """
        if not set1 or not set2:
            return 0.0
        
        # Calcul de l'intersection des deux ensembles
        intersection_size: int = len(set1.intersection(set2))
        
        # Taille du plus petit ensemble
        min_size: int = min(len(set1), len(set2))
        
        # Coefficient de chevauchement
        overlap_coefficient: float = intersection_size / min_size
        
        return overlap_coefficient


class SorensenDice(Distance):
	
	def __init__(self):
		super().__init__()
		
	def compute(self,str1 :str, str2 :str) -> float:
		# Convert strings to sets of bigrams
		bigrams1 = {str1[i:i+2] for i in range(len(str1) - 1)}
		bigrams2 = {str2[i:i+2] for i in range(len(str2) - 1)}
    
		# Calculate the intersection and the sizes of the sets
		intersection = len(bigrams1 & bigrams2)
		size1 = len(bigrams1)
		size2 = len(bigrams2)
    
		# Calculate the Sørensen-Dice coefficient
		sorensen_dice_coeff = 2 * intersection / (size1 + size2)
    
		# The distance is 1 minus the coefficient
		distance = 1 - sorensen_dice_coeff
    
		return distance
		
	def exemple(self):
		self.obj1_exemple = "night"
		self.obj2_exemple = "nacht"

		super().exemple()
		
from typing import List, Dict
from collections import Counter
import math

class BagOfWordsDistance:
    def __init__(self) -> None:
        """
        Initialisation de la classe BagOfWordsDistance.
        """
        pass

    def compute(self, text1: str, text2: str) -> float:
        """
        Calcule la distance entre deux textes en utilisant la représentation Bag-of-Words.

        :param text1: Premier texte.
        :param text2: Deuxième texte.
        :return: Distance entre les deux textes, entre 0 et 1.
        """
        # Création des sacs de mots pour les deux textes
        bow1: Dict[str, int] = self._text_to_bow(text1)
        bow2: Dict[str, int] = self._text_to_bow(text2)

        # Union de tous les mots dans les deux textes
        all_words: List[str] = list(set(bow1.keys()).union(set(bow2.keys())))

        # Vecteurs de fréquences des mots pour chaque texte
        vec1: List[int] = [bow1.get(word, 0) for word in all_words]
        vec2: List[int] = [bow2.get(word, 0) for word in all_words]

        # Calcul de la distance entre les deux vecteurs (utilisation de la distance euclidienne ici)
        distance: float = Euclidean().compute(vec1, vec2)
        
        return distance

    def _text_to_bow(self, text: str) -> Dict[str, int]:
        """
        Convertit un texte en un sac de mots (Bag of Words).

        :param text: Texte à convertir.
        :return: Dictionnaire représentant la fréquence de chaque mot dans le texte.
        """
        # Découper le texte en mots
        words: List[str] = text.lower().split()
        
        # Créer un sac de mots avec les fréquences de chaque mot
        bow: Dict[str, int] = dict(Counter(words))
        
        return bow





