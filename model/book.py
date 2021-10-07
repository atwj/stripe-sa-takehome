class Book:
    def __init__(self, id, title, author, desc, amount, image_path):
        self._id = id
        self._title = title
        self._author = author
        self._desc = desc
        self._amount = amount
        self._image_path = image_path

    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author
    
    @property
    def desc(self):
        return self._desc
    
    @property
    def amount(self):
        return self._amount

    @property
    def image_path(self):
        return self._image_path

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "desc": self.desc,
            "amount": self.amount,
            "image_path": self.image_path
        }