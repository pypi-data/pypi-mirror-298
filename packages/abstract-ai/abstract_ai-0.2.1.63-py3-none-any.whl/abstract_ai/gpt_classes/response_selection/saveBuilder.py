from abstract_utilities import (os,get_date,
                                mkdirs,
                                safe_json_loads,
                                safe_read_from_json)
import json
def mkDirPath(*args):
    for i,arg in enumerate(args):
        if i ==0:
            path = arg
        else:
            path = os.path.join(os.getcwd(), arg)
        mkdirs(path)
    return path
class SaveManager:
    """
    Manages the saving of data. This class should provide methods to specify where (e.g., what database or file) and how (e.g., in what format) data should be saved.
    """
    def __init__(self, data={},title:str=None,directory:str=None,model:str='default')->None:
        self.title=title
        self.model=model
        self.date = get_date()
        self.directory = directory
        self.file_path = self.create_unique_file_name()
        if data:
            self.data = safe_json_loads(data)
            self.data['file_path']=self.file_path
            self.data['title']=self.title
            self.data['model']=self.model
            self.save_to_file(data = data,file_path = self.file_path)
    def create_unique_file_name(self,directory=None,title=None) -> str:
        title = title or self.title
        directory = directory or self.directory
        # Sanitize and shorten the title
        sanitized_title = self.sanitize_title(title)

        # Generate base file name
        base_name = f"{sanitized_title}.json"
        
        # Check for uniqueness and append index if needed
        unique_name = base_name
        for i in range(len(os.listdir(directory))+1):
            file_path = os.path.join(directory, unique_name)
            if not os.path.exists(file_path):
                return file_path
            unique_name = f"{sanitized_title}_{i}.json"
    @staticmethod
    def sanitize_title(title: str) -> str:
        if title:
            # Replace spaces and special characters
            title = str(title).replace(" ", "_").replace(":", "_")

            # Limit the length of the title
            #max_length = max_title
            #if len(title) > max_length:
            #    title = title[:max_length]

            return title
    def save_to_file(self, data:dict, file_path:str)->None:
        # Assuming `data` is already a dictionary, we convert it to a JSON string and save.
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    @staticmethod
    def read_saved_json(file_path:str)->dict:
        # Use 'safe_read_from_json' which is presumed to handle errors and return JSON
        return safe_read_from_json(file_path)
