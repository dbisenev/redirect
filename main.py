from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from urllib.parse import urlparse, parse_qs
import re

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Steam OpenID Callback Server"}

@app.get("/steamcallback")
async def steam_callback(request: Request):
    query_params = urlparse(str(request.url)).query
    params = parse_qs(query_params)

    if 'openid.claimed_id' not in params:
        raise HTTPException(status_code=400, detail="Invalid response from Steam")

    steam_id_url = params['openid.claimed_id'][0]
    steam_id_match = re.search(r'/id/(\d+)', steam_id_url)
    if not steam_id_match:
        raise HTTPException(status_code=400, detail="Invalid Steam ID format")

    steam_id = steam_id_match.group(1)


    android_intent_url = (
        f"intent://steam?steamId={steam_id}#Intent;"
        "scheme=myapp;"
        "package=com.example.myapp;"
        "end;"
    )
    
    return RedirectResponse(url=android_intent_url)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
