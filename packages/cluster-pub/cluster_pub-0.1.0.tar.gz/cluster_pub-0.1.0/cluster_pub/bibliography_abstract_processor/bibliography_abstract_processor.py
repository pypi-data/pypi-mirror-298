import re
from typing import List
from multiprocessing import cpu_count, Pool
from time import time
from unicodedata import normalize
from logging import getLogger

from ..bibliography_parsers.schemas import BibliographyFileData
from .schemas import ProcessedBibliographyFileData

logger = getLogger(__name__)


class BibliographyAbstractProcessor:

    _numbers_to_letter_mapping = str.maketrans("0123456789", "ABCDEFGHIJ")

    def process_bibliography_file_entries(
        self, bibliography_file_entries: List[BibliographyFileData]
    ) -> List[ProcessedBibliographyFileData]:
        initial_time = time()

        logger.info("Starting to pre-process bibliography entries content")

        with Pool(processes=cpu_count()) as process_executor:

            processed_bibliography_file_results = process_executor.map(
                self.process_bibliography_file_entry,
                bibliography_file_entries,
                chunksize=50,
            )

        finish_time = time() - initial_time
        logger.info(f"Time to pre-process entries: {finish_time}")

        logger.info("Pre-processed entries successfully")

        return processed_bibliography_file_results

    def process_bibliography_file_entry(
        self, bibliography_file_entry: BibliographyFileData
    ) -> ProcessedBibliographyFileData:

        processed_bibliography_abstract = self.process_bibliography_abstract(
            bibliography_abstract=bibliography_file_entry["abstract"]
        )

        processed_bibliography_file_entry = ProcessedBibliographyFileData(
            title=bibliography_file_entry["title"],
            processed_abstract=processed_bibliography_abstract,
        )

        return processed_bibliography_file_entry

    def process_bibliography_abstract(self, bibliography_abstract: str) -> str:
        processed_bibliography_abstract = re.sub(r"[\W]", "", bibliography_abstract)

        processed_bibliography_abstract = self.decode_abstract(
            abstract=processed_bibliography_abstract
        )

        processed_bibliography_abstract = processed_bibliography_abstract.translate(
            self._numbers_to_letter_mapping
        )

        return processed_bibliography_abstract.upper()

    def decode_abstract(self, abstract: str) -> str:
        initially_decoded_abstract = normalize("NFD", abstract)
        bytes_processed_abstract = initially_decoded_abstract.encode("ascii", "ignore")

        decoded_abstract = bytes_processed_abstract.decode("UTF-8")

        return decoded_abstract
