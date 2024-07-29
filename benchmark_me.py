#!/usr/bin/env python3

import weakref
from argparse import ArgumentParser
from spinedb_api import DatabaseMapping
from spinedb_api.exception import SpineDBVersionError



class MyDBMap:
    def __init__(self, url: str):
        self.db = self.load_db(url)
        self._finalizer = weakref.finalize(self, self.clean_up)
        self.data = {}

    def load_db(self, url: str) -> None:
        try:
            db = DatabaseMapping(f"sqlite:///{url}")
        except SpineDBVersionError:
            print("Database version not matching, trying to upgrade ...")
            db = DatabaseMapping(f"sqlite:///{url}", upgrade=True)
            print("Upgrade successful!")

        return db

    def clean_up(self) -> None:
        print("Closing DB connection ...")
        self.db.close()
        print("... closed DB connection")



if __name__ == "__main__":
    parser = ArgumentParser("Read Spine DB")
    parser.add_argument("db_url", help="DB url")
    opts = parser.parse_args()

    handle = MyDBMap(opts.db_url)
    # ts = handle.get_ts("unit_flow")  # 4
    # ts = handle.get_ts("cost_t")  # 268
