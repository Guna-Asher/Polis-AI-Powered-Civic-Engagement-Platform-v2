from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import uuid
from typing import List
import datetime

# Import from shared models
import sys
import os
sys.path.append('/app/shared')
from models import *

app = FastAPI(title="Polis API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
feedback_db = {}

@app.get("/")
async def root():
    return {"message": "Polis API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

@app.post("/api/legislation/upload", response_model=LegislationSummary)
async def upload_legislation(file: UploadFile = File(...)):
    """Upload and process legislation document"""
    try:
        content = await file.read()
        
        # Simulate AI processing
        legislation_id = str(uuid.uuid4())
        summary = LegislationSummary(
            title="Sample Legislation Act 2024",
            summary="This legislation aims to improve public infrastructure and environmental standards. It represents a comprehensive approach to addressing climate change while promoting economic growth through sustainable practices.",
            key_points=[
                "Increases funding for green energy projects by $500M",
                "Establishes new environmental protection standards for 2030",
                "Creates tax incentives for sustainable businesses"
            ],
            clauses=[
                {"id": "clause_1", "text": "Allocate $500M for renewable energy research and development programs"},
                {"id": "clause_2", "text": "Set carbon emission reduction targets of 50% by 2030 compared to 2020 levels"},
                {"id": "clause_3", "text": "Provide tax credits of up to $7,500 for electric vehicle purchases"}
            ]
        )
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback/submit")
async def submit_feedback(feedback: List[ClauseFeedback]):
    """Submit structured feedback for legislation"""
    try:
        feedback_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        
        feedback_data = {
            "id": feedback_id,
            "timestamp": timestamp,
            "feedback": [f.dict() for f in feedback]
        }
        
        feedback_db[feedback_id] = feedback_data
        print(f"Received feedback: {feedback_data}")  # Debug log
        
        return {"message": "Feedback submitted successfully", "id": feedback_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/pulse")
async def get_civic_pulse():
    """Get aggregated civic pulse data"""
    total_feedback = len(feedback_db)
    
    # Calculate real sentiment distribution from stored feedback
    sentiment_counts = {
        SentimentLevel.STRONGLY_OPPOSE: 0,
        SentimentLevel.OPPOSE: 0,
        SentimentLevel.NEUTRAL: 0,
        SentimentLevel.SUPPORT: 0,
        SentimentLevel.STRONGLY_SUPPORT: 0
    }
    
    # Aggregate sentiments from stored feedback
    for feedback_id, data in feedback_db.items():
        for clause_feedback in data['feedback']:
            sentiment = clause_feedback['sentiment']
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1
    
    total_sentiments = sum(sentiment_counts.values()) or 1  # Avoid division by zero
    sentiment_distribution = {
        sentiment: count / total_sentiments 
        for sentiment, count in sentiment_counts.items()
    }
    
    # Simulate tag cloud and clause sentiments
    pulse_data = CivicPulseData(
        total_feedback=total_feedback,
        sentiment_distribution=sentiment_distribution,
        tag_cloud={"#CostConcern": 45, "#EnvironmentalBenefit": 67, "#ImplementationIssue": 23},
        clause_sentiments={
            "clause_1": {
                SentimentLevel.STRONGLY_OPPOSE: 3,
                SentimentLevel.OPPOSE: 5,
                SentimentLevel.NEUTRAL: 10,
                SentimentLevel.SUPPORT: 25,
                SentimentLevel.STRONGLY_SUPPORT: 15
            },
            "clause_2": {
                SentimentLevel.STRONGLY_OPPOSE: 2,
                SentimentLevel.OPPOSE: 8,
                SentimentLevel.NEUTRAL: 15,
                SentimentLevel.SUPPORT: 20,
                SentimentLevel.STRONGLY_SUPPORT: 12
            }
        }
    )
    
    return pulse_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)