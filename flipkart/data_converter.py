import pandas as pd 
from langchain_core.documents import Document

class DataConverter:
    def __init__(self, file_path:str):
        self.file_path = file_path
        
    def convert(self):
        df = pd.read_csv(self.file_path)[["product_title", "rating", "review"]]
        
        docs = [
            Document(page_content=f"Review: {row['review']}\nRating: {row['rating']}", metadata= {"product_name" : row["product_title"]})
            for _,row in df.iterrows()
        ]
        
        return docs