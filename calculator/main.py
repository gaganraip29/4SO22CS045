
from fastapi import FastAPI, HTTPException
from typing import List
app = FastAPI(title="calculator")


receivedNumbers:List[float]=[]
class NumbersInput(BaseModel):
    num:List[float]

from pydantic import BaseModel
@app.get("/")
async def read_root():
    return {"message": "Average Calculator running"}

@app.post("/average")
async def calculate_average_stage1(data: NumbersInput):
    global receivedNumbers

    new_num = data.num

    if not new_num:
        raise HTTPException(statusCode=400, message="Please provide a list of numbers.")

    
    for num in new_num:
        receivedNumbers.append(float(num)) 

    current_sum = 0
    count = 0
   
    for n in receivedNumbers:
        current_sum += n
        count += 1

    avg = 0.0
    if count > 0:
        avg = current_sum / count
    

    return {
        "numbers recieved": new_num,
        "stored numbers": receivedNumbers,
        "average of all": round(avg, 2)
    }
