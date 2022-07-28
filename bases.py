from sqlalchemy import Column, ForeignKey, Integer, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import relationship  
from sqlalchemy import create_engine  

engine = create_engine("sqlite:///base.db", echo=True)

Base = declarative_base()  

class Comments(Base):  
    __tablename__ = 'Comments'  

    number = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    name_href = Column(String(250), nullable=False)
    text_post = Column(String(250), nullable=False)
    avatar = Column(String, nullable=False)

    def __repr__(self):
        return '<Comments %r>' % self.number

Base.metadata.create_all(engine)   