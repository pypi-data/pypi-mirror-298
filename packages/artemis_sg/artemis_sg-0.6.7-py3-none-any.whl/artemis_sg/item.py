import logging
import re

import isbnlib

from artemis_sg.config import CFG


class Item:
    def __init__(self, keys, values, row_num, isbn_key):
        clean_keys = []
        for x in keys:
            if x:
                clean_keys.append(str(x).strip().upper())
        self.data = dict(zip(clean_keys, values))
        self.data_row_num = row_num
        self.isbn_key = isbn_key
        self.isbn = self.validate_isbn(self.data[isbn_key])
        self.isbn10 = isbnlib.to_isbn10(self.isbn)
        self.image_urls = []
        if "DESCRIPTION" not in self.data:
            self.data["DESCRIPTION"] = ""
        if "DIMENSION" not in self.data:
            self.data["DIMENSION"] = ""
        self._sort_data()

    def _sort_data(self):
        namespace = f"{type(self).__name__}.{self._sort_data.__name__}"

        def sort_order(e):
            defined_order = CFG["asg"]["item"]["sort_order"]
            if e in defined_order:
                return defined_order.index(e)
            return 99

        sorted_keys = list(self.data.keys())
        # sort by defined order
        sorted_keys.sort(key=sort_order)
        # move ISBN and DESCRIPTION to end of list
        sorted_keys.sort(key=self.isbn_key.__eq__)
        sorted_keys.sort(key="DESCRIPTION".__eq__)
        logging.debug(f"{namespace}: Sorted keys: {sorted_keys}")

        sorted_data = {key: self.data[key] for key in sorted_keys}
        self.data = sorted_data

    def validate_isbn(self, isbn):
        namespace = f"{type(self).__name__}.{self.validate_isbn.__name__}"
        valid_isbn = ""
        mod_isbn = str(isbn)
        if isbnlib.is_isbn13(mod_isbn) or isbnlib.is_isbn10(mod_isbn):
            valid_isbn = isbnlib.to_isbn13(mod_isbn)
        else:
            # look for formula value
            m = re.search('="(.*)"', mod_isbn)
            if m:
                mod_isbn = m.group(1)
            # look for float value
            mod_isbn = mod_isbn.split(".", 1)[0]
            # look for value with missing zero(s)
            mod_isbn = mod_isbn.zfill(10)
            if isbnlib.is_isbn13(mod_isbn) or isbnlib.is_isbn10(mod_isbn):
                valid_isbn = isbnlib.to_isbn13(mod_isbn)
            else:
                logging.error(f"{namespace}: Err reading isbn '{isbn}'")
        return valid_isbn
