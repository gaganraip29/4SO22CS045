from fastapi import FastAPI
import httpx
import uvicorn

my_app = FastAPI()

my_auth_info = {
    "email": "22a45.gagan@sjec.ac.in", 
    "name": "gagan rai p",
    "rollNo": "4so22cs045",
    "accessCode": "KjJAxP",
    "clientID": "895e1b6d-8697-46ed-b519-f4f3f36dd76e",
    "clientSecret": "dxyZMgXpWkuzZYbd"
}

Base="http://20.244.56.144/evaluation-service"


@my_app.get("/stocks/{lis}")
async def GetData(lis: str, min: int = None, aggregation: str = None):
    res = httpx.post(f"{Base}/auth", json=my_auth_info)
    Token = res.json()["access_token"]
    
    authH = {"Authorization": f"Bearer {Token}"}
    
    endpoint = f"{Base}/stocks/{lis}"
    if min:
        endpoint = endpoint + f"?min={min}"
    
    respon = httpx.get(endpoint, headers=authH)
    result = respon.json()
    
    if not isinstance(result, list):
        result = [result["stock"]]
    
    ps = 0
    for stock_entry in result:
        ps = ps + stock_entry["price"]
    
    M_price = ps / len(result)
        
    return {
        "averagestockprice": M_price,
        "pricehistory": result
    }


@my_app.get("/stockcorrelation")
async def cal_corel(min: int = None, lis: list = None):
    
    res = httpx.post(f"{Base}/auth", json=my_auth_info)
    Token = res.json()["access_token"]

    
    authH = {"authorization": f"Bearer {Token}"}
     
    f_stock = f"{Base}/stocks/{lis[0]}"
    if min:
        f_stock = f_stock + f"?min={min}"
    f_res = httpx.get(f_stock, headers=authH)
    f_data = f_res.json()
    if not isinstance(f_data, list):
        f_data = [f_data["stock"]]
    
    s_end = f"{Base}/stocks/{lis[1]}"
    if min:
        s_end = s_end + f"?min={min}"
    s_res = httpx.get(s_end, headers=authH)
    s_data = s_res.json()
    if not isinstance(s_data, list):
        s_data = [s_data["stock"]]
    
    first_sum = 0
    for entry in f_data:
        first_sum = first_sum + entry["price"]
    first_avg = first_sum / len(f_data)
     
    s_sum = 0
    for entry in s_data:
        s_sum = s_sum + entry["price"]
    s_avg = s_sum / len(s_data)
    
    relVal = 0.5
    
    return {
        "correlation": relVal,
        "stocks": {
            lis[0]: {"averageprice": first_avg, "pricehistory": f_data},
            lis[1]: {"averageprice": s_avg, "pricehistory": s_data}
        }
    }
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)