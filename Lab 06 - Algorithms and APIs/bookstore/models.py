"""Pydantic Models and Data Validations for Bookstore Service."""
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class Book(BaseModel):
    """Book Model Entity with Field and custom validators"""

    id: int = Field(..., description="Unique book identifier")
    title: str = Field(..., min_length=1, description="Book title")
    author: str = Field(..., min_length=1, description="Book Author")
    year: int = Field(
        ...,
        ge=1450,
        description="Posting year"
    )
    isbn: str = Field(..., description="ISBN Code with 10 or 13 alphanumeric chars")

    @field_validator("year")
    @classmethod
    def validate_year_not_future(cls, value:int) -> int:
        """Validate that post date is not greater than present."""
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError
            (f"El año de publicación ({value}) no puede ser mayor al actual ({current_year}).")
        return value

    @field_validator("isbn")
    @classmethod
    def validate_isbn_length(cls, value:str) -> str:
        """Function to validate isbn length code."""
        clean_isbn = value.replace("-","").strip()
        if not (len(clean_isbn) in (10, 13) and clean_isbn.isalnum()):
            raise ValueError("Formato ISBN Inválido. Debe contener entre 10 a 13 caracteres alfanuméricos.") 
        return value
