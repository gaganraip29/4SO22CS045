from fastapi import FastAPI
from pydantic import BaseModel, conlist
from typing import List

win_size = 10

app = FastAPI(
    title="Average Calculator (WIP)",
    description="Calculates a windowed average of numbers. Nearing completion.",
    version="0.8.9"
)

present_window: List[float] = []

class numinp(BaseModel):
    num: conlist(float, min_length=1)

@app.get("/")
async def read_root():
    return {"message": "average calculator"}

@app.post("/average")
async def win_avg(data: numinp):
    global present_window
    
    prevWindow = list(present_window)
    new = data.num
    
    for n in new:
        present_window.append(n)
    
    if len(present_window) > win_size:
        rem = len(present_window) - win_size
        present_window = present_window[rem:]
    
    present = list(present_window)
    finalAverage = 0.0
    
    if present:
        total_sum = sum(present)  # Changed variable name from sum to total_sum
        nCount = len(present)
        finalAverage = total_sum / nCount
    
    return {
        "previous state of window": prevWindow,
        "numbers in new request": new,
        "present content in the window": present,
        "average of the present window": round(finalAverage, 2)
    }