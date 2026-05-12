import json
import os
from bookmark import Bookmark
from typing import List
from dataclasses import dataclass, asdict




class BookmarkManager:

    def __init__(self):
        self.filepath = "bookmark.json"
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def load(self,filepath):
        results = []
        if filepath in self.data:
            for i in self.data[filepath]:
                bm = Bookmark(label=i["label"],timestamp=i["timestamp"],filepath=i["filepath"])
                results.append(bm)
            return results
        else:
            return[]
        

    def save(self,filepath,bookmarks_list):
        converted = []

        for i in bookmarks_list:
            bm = asdict(i)
            converted.append(bm)

        self.data[filepath] = converted
        
        with open(self.filepath, 'w') as file:
            json.dump(self.data, file)


    def add_bookmark(self,new_bookmark):
        loading = self.load(new_bookmark.filepath)
        loading.append(new_bookmark)
        self.save(new_bookmark.filepath, loading)

    def delete_bookmark(self,filepath,timestamp):
        loading = self.load(filepath)
        updated = []
        for i in loading:
            if i.timestamp != timestamp:
                updated.append(i)
        self.save(filepath,updated)


    def rename_bookmark(self,filepath,new_label,timestamp):
        loading = self.load(filepath)
        for i in loading:
            if i.timestamp == timestamp:
                i.label = new_label
        self.save(filepath,loading)




            

            
        