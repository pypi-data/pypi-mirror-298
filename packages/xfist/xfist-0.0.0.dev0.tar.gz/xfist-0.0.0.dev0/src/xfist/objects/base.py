from pathlib import Path
import shutil

class Base:
    def __init__(self, path: Path):
        self._path = path
    
    def exists(self):
        self._path.exists()
    
    def _delete(self, force=False):
        pass