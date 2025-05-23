import fitz  # PyMuPDF
import os
from typing import List, Dict, Any

class FileLoader:
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths
        self.documents = []

    def load_all(self) -> List[Dict[str, Any]]:
        for path in self.file_paths:
            ext = os.path.splitext(path)[-1].lower()
            if ext == ".pdf":
                self._load_pdf(path)
            elif ext == ".txt":
                self._load_txt(path)
            else:
                print(f"Unsupported file type: {path}")
        return self.documents

    def _load_pdf(self, path: str):
        doc = fitz.open(path)
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            images = page.get_images(full=True)
            image_refs = []

            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                img_ext = base_image["ext"]
                image_name = f"{os.path.basename(path)}_page{page_num}_img{img_index}.{img_ext}"
                image_path = os.path.join("data", "images", image_name)

                # Save image locally
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)

                image_refs.append({
                    "page": page_num,
                    "path": image_path
                })

            self.documents.append({
                "filename": os.path.basename(path),
                "page": page_num,
                "type": "pdf",
                "text": text.strip(),
                "images": image_refs
            })

    def _load_txt(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.documents.append({
            "filename": os.path.basename(path),
            "type": "txt",
            "text": content.strip(),
            "images": [],
            "page": None
        })
