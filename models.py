from pydantic import BaseModel

class Email(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    url: str
    user: str
    mailtext: str
    mailaddress: str

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "url": self.url,
            "user": self.user,
            "mailtext": self.mailtext,
            "mailaddress": self.mailaddress
        }