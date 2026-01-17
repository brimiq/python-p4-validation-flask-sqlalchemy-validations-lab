from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self, name=None, phone_number=None, **kwargs):
        # Validate name
        if not name or name.strip() == '':
            raise ValueError('Author must have a name')
        # Validate phone number
        if phone_number is not None and not re.match(r'^\d{10}$', phone_number):
            raise ValueError('Phone number must be exactly 10 digits')
        # Check unique name constraint
        existing = Author.query.filter(Author.name == name).first()
        if existing:
            raise ValueError('Author name must be unique')
        super().__init__(name=name, phone_number=phone_number, **kwargs)

    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip() == '':
            raise ValueError('Author must have a name')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number is None:
            return phone_number
        if not re.match(r'^\d{10}$', phone_number):
            raise ValueError('Phone number must be exactly 10 digits')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self, title=None, content=None, category=None, summary=None, **kwargs):
        # Validate title
        if not title or title.strip() == '':
            raise ValueError('Post must have a title')
        # Validate content length
        if content is not None and len(content) < 250:
            # Check clickbait only if content is too short
            clickbait_patterns = [r'^Why', r'^Top', r'^Secret']
            for pattern in clickbait_patterns:
                if re.search(pattern, title, re.IGNORECASE):
                    raise ValueError('Title must not be clickbait')
            raise ValueError('Content must be at least 250 characters')
        # Validate category
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be Fiction or Non-Fiction')
        # Validate summary length
        if summary is not None and len(summary) > 250:
            raise ValueError('Summary must be at most 250 characters')
        super().__init__(title=title, content=content, category=category, summary=summary, **kwargs)

    @validates('title')
    def validate_title(self, key, title):
        if not title or title.strip() == '':
            raise ValueError('Post must have a name')
        clickbait_patterns = [r'^Why', r'^Top', r'^Secret']
        for pattern in clickbait_patterns:
            if re.search(pattern, title, re.IGNORECASE):
                raise ValueError('Title must not be clickbait')
        return title

    @validates('content')
    def validate_content(self, key, content):
        if content is None:
            return content
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary is None:
            return summary
        if len(summary) > 250:
            raise ValueError('Summary must be at most 250 characters')
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be Fiction or Non-Fiction')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

