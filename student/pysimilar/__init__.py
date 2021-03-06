import os
import sys
from pathlib import Path
from typing import Union, List, Dict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from docx import Document
from os.path import splitext

class PlagiarismCheck(object):

    VALID_EXTENSION: List[str] = ['.doc', '.txt', '.docx']
    @property
    def extensions(self) -> List[str]:
        return self.VALID_EXTENSION

    @extensions.setter
    def extensions(self, new_extensions: Union[str, List[str]]):

        if not isinstance(new_extensions, (str, list)):
            raise TypeError(
                f'New extensions must be of either type <str> or <list> not {type(new_extensions)}')
        if isinstance(new_extensions, str):
            new_extensions: List[str] = [new_extensions]
        self.VALID_EXTENSION = new_extensions

    def get_files(self, path_to_files: Union[Path, str]) -> List[str]:
    

        all_files_and_dirs = os.listdir(path_to_files)
        available_files: List[str] = []
        for file_or_dir in all_files_and_dirs:
            full_path = os.path.join(path_to_files, file_or_dir)
            if os.path.isfile((full_path)) and any([full_path.endswith(ext) for ext in self.VALID_EXTENSION]):
                available_files.append(full_path)
        return available_files

    @staticmethod
    def load_file(path_to_file: Union[Path, str]):
        file_name,extension = splitext(path_to_file)
        if extension in ['.docx', '.doc']:
            doc = Document(path_to_file)
            allText = []
            for docpara in doc.paragraphs:
                allText.append(docpara.text)
            return '\n'.join(allText)

        with open(path_to_file, 'r') as document:
            content = document.read()
        return content

    def load_files(self, path_to_folder: Union[Path, str]):
        path_to_files: List[str] = self.get_files(path_to_folder)
        load_documents: List[str] = [self.load_file(path_to_document)
                                     for path_to_document in path_to_files]
        file_names = [path_to_file.split('/')[-1]
                      for path_to_file in path_to_files]
        document_dictionary = dict(zip(file_names, load_documents))
        return document_dictionary

    def compare(self, string_i: Union[str, Path], string_j: Union[str, Path], isfile=False) -> float:

        if not isinstance(string_i, (str, Path)) or not isinstance(string_j, (str, Path)):
            raise TypeError(
                'Both string i and string j must be of type either string or Path')

        if isfile:
            string_i, string_j = self.load_file(
                string_i), self.load_file(string_j)

        corpus = [string_i, string_j]
        vector_i, vector_j = self.string_to_vector(corpus)
        return self.compute_similarity(vector_i, vector_j)

    def compare_documents(self, path_to_documents: Union[str, Path], sort=True, ascending=False) -> list:
        
        if not os.path.exists(path_to_documents):
            raise FileNotFoundError(
                f'Path <{path_to_documents}> Does not exist')

        loaded_documents: Dict = self.load_files(path_to_documents)
        vectorized_documents = self.vectorize_dict(loaded_documents)
        compared_documents: List[set] = []
        comparison_results: List[list] = []
        for current_document_name, current_content in vectorized_documents.items():
            for document_name, content in vectorized_documents.items():
                current_comparison = f'{current_document_name} vs {document_name}'
                if (current_document_name == document_name) or (set(current_comparison) in compared_documents):
                    continue
                result = self.compute_similarity(current_content, content)
                displayable_result = [current_comparison, result]
                comparison_results.append(displayable_result)
                compared_documents.append(set(current_comparison))

        if not sort:
            return comparison_results

        sorted_results = sorted(
            comparison_results, key=lambda x: x[1], reverse=not ascending)
        return sorted_results

    def compute_similarity(self, vector_a: list, vector_b: list) -> float:
        

        return cosine_similarity([vector_a, vector_b])[0][1]

    def vectorize_dict(self, documents: Dict) -> Dict:
       
        file_names = list(documents.keys())
        corpus = list(documents.values())
        vectorized_corpus = self.string_to_vector(corpus)
        return dict(zip(file_names, vectorized_corpus))

    def string_to_vector(self, corpus: List[str]):
       
        return TfidfVectorizer().fit_transform(corpus).toarray()


sys.modules[__name__] = PlagiarismCheck()