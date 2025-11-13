import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Event, Member, Social, ClubInfo

app = FastAPI(title="College Club API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "College Club API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                response["collections"] = db.list_collection_names()
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but error: {str(e)[:80]}"
        else:
            response["database"] = "❌ Not Initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"
    return response

# --------- Club Info ---------
@app.get("/api/club", response_model=List[ClubInfo])
def get_club_info():
    try:
        docs = get_documents("clubinfo")
        return [ClubInfo(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/club")
def create_club_info(info: ClubInfo):
    try:
        _id = create_document("clubinfo", info)
        return {"inserted_id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------- Events ---------
@app.get("/api/events", response_model=List[Event])
def list_events():
    try:
        docs = get_documents("event")
        return [Event(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/events")
def create_event(event: Event):
    try:
        _id = create_document("event", event)
        return {"inserted_id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------- Team / Members ---------
@app.get("/api/team", response_model=List[Member])
def list_team():
    try:
        docs = get_documents("member")
        return [Member(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/team")
def create_member(member: Member):
    try:
        _id = create_document("member", member)
        return {"inserted_id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------- Socials ---------
@app.get("/api/socials", response_model=List[Social])
def list_socials():
    try:
        docs = get_documents("social")
        return [Social(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/socials")
def create_social(social: Social):
    try:
        _id = create_document("social", social)
        return {"inserted_id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
