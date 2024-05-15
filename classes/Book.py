'''
  This module contains the class Book, which is used to represent a book.
'''
class Book():
  ''' 
  Represents a book.
  '''
  def __init__(
    self,
    book_id,
    name,
    authors,
    published_date,
    description,
    page_count,
    categories,
    average_rating,
    thumbnail,
    publisher,
    language,
    url
  ):
    self.book_id = book_id
    self.name = name
    self.published_date = published_date
    self.description = description
    self.page_count = page_count
    self.average_rating = average_rating
    self.thumbnail = thumbnail
    self.language = language
    self.publisher = publisher
    self.authors = ", ".join(authors) if isinstance(authors, list) else authors
    self.categories = ", ".join(categories) if isinstance(categories, list) else categories
    self.url = url

  @classmethod
  def from_dict(cls, item, volume_info):
    ''' Creates a new instance of a book from the data provided in the dictionary.

    Parameters
    ----------
    item: dict
        The dictionary containing the data of the book.
    volume_info: dict
        The dictionary containing the volume information of the book.
    return: :class:`Book`
    '''
    return cls(
      book_id=item.get("id", ""),
      name=volume_info.get("title", ""),
      authors=volume_info.get("authors", " - "),
      published_date=volume_info.get("publishedDate", " -/-/- "),
      description=volume_info.get("description", " - "),
      page_count=volume_info.get("pageCount", 0),
      categories=volume_info.get("categories", []),
      language=volume_info.get("language", ""),
      thumbnail=volume_info.get("imageLinks", {}).get("thumbnail", None),
      average_rating=volume_info.get("averageRating", 0),
      publisher=volume_info.get("publisher", " - "),
      url = volume_info.get("canonicalVolumeLink", " - ")
    )
