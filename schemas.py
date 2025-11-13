"""
Database Schemas for College Club Website

Each Pydantic model maps to a MongoDB collection using the lowercase class name.
- Event -> "event"
- Member -> "member"
- Social -> "social"
- ClubInfo -> "clubinfo"
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class Event(BaseModel):
    title: str = Field(..., description="Event title")
    date: str = Field(..., description="Event date in YYYY-MM-DD or human readable")
    location: Optional[str] = Field(None, description="Where the event took place")
    description: Optional[str] = Field(None, description="Short summary of the event")
    cover_image: Optional[HttpUrl] = Field(None, description="Cover image URL")
    gallery: Optional[List[HttpUrl]] = Field(default_factory=list, description="List of image URLs for glimpses")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags or categories")

class Member(BaseModel):
    name: str = Field(..., description="Full name")
    role: str = Field(..., description="Role in the club (e.g., President)")
    bio: Optional[str] = Field(None, description="Short bio")
    avatar: Optional[HttpUrl] = Field(None, description="Profile image URL")
    socials: Optional[dict] = Field(default_factory=dict, description="Map of social handles/links")

class Social(BaseModel):
    platform: str = Field(..., description="Platform name, e.g., Instagram, Twitter, LinkedIn")
    url: HttpUrl = Field(..., description="Profile URL")
    handle: Optional[str] = Field(None, description="@handle if any")

class ClubInfo(BaseModel):
    name: str = Field(..., description="Club name")
    tagline: Optional[str] = Field(None, description="Short tagline")
    about: Optional[str] = Field(None, description="About the club")
    vision: Optional[str] = Field(None, description="Vision statement")
    mission: Optional[str] = Field(None, description="Mission statement")
    primary_color: Optional[str] = Field(None, description="Primary brand color hex, e.g., #1e90ff")
    secondary_color: Optional[str] = Field(None, description="Secondary brand color hex")
