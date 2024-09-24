from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()


class Reference(BaseModel):
    file_name: str
    file_link: str
    page_numbers: List[int] = Field(default_factory=list)
    sheet_names: List[str] = Field(default_factory=list)

    def to_md(self) -> str:
        show_reference_hyperlink = os.environ.get(
            "BOTRUN_ASK_FOLDER_SHOW_REFERENCE_HYPERLINK", "True"
        )
        show_reference_hyperlink = show_reference_hyperlink.lower() == "true"
        ref_name = self.file_name
        if self.page_numbers:
            pages = ", ".join(map(str, self.page_numbers))
            ref_name += f" - 第 {pages} 頁"
        elif self.sheet_names:
            sheets = ", ".join(self.sheet_names)
            ref_name += f" - 頁籤：{sheets}"
        if show_reference_hyperlink:
            return f"- [{ref_name}]({self.file_link})"
        else:
            return f"- {ref_name}"


class References(BaseModel):
    references: List[Reference] = Field(default_factory=list)

    def to_md(self) -> str:
        if len(self.references) == 0:
            return ""
        return f"參考來源：\n" + "\n".join(ref.to_md() for ref in self.references)
