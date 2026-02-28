import httpx
from fastapi import FastAPI, Request, Response, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title="Bookstore API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def proxy_request(target_url: str, request: Request):
    async with httpx.AsyncClient(timeout=10.0) as client:
        path = request.scope['path'].replace("//", "/")
            
        url = f"{target_url}{path}"
        if request.query_params:
            url += f"?{request.query_params}"
            
        try:
            rp_req = client.build_request(
                request.method,
                url,
                headers=request.headers.raw,
                content=await request.body()
            )
            rp_resp = await client.send(rp_req, stream=True)
            return Response(
                content=await rp_resp.aread(),
                status_code=rp_resp.status_code,
                headers=dict(rp_resp.headers)
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Downstream Service Unavailable")# --- PROXY ROUTES WITH PATH PARAMETER DECLARED ---


# --- AUTH SERVICE ---
@app.post("/auth/{path:path}", tags=["Auth"])
async def auth_post(request: Request, path: str = Path(...)):
    return await proxy_request(settings.AUTH_SERVICE_URL, request)

@app.get("/auth/{path:path}", tags=["Auth"])
async def auth_get(request: Request, path: str = Path(...)):
    return await proxy_request(settings.AUTH_SERVICE_URL, request)

# --- BOOK SERVICE ---
@app.get("/books/{path:path}", tags=["Books"])
async def books_get(request: Request, path: str = Path(...)):
    return await proxy_request(settings.BOOK_SERVICE_URL, request)

@app.post("/books/{path:path}", tags=["Books"])
async def books_post(request: Request, path: str = Path(...)):
    return await proxy_request(settings.BOOK_SERVICE_URL, request)

@app.put("/books/{path:path}", tags=["Books"])
async def books_put(request: Request, path: str = Path(...)):
    return await proxy_request(settings.BOOK_SERVICE_URL, request)

# --- ORDER SERVICE ---
@app.post("/orders/{path:path}", tags=["Orders"])
async def orders_post(request: Request, path: str = Path(...)):
    return await proxy_request(settings.ORDER_SERVICE_URL, request)

@app.get("/orders/{path:path}", tags=["Orders"])
async def orders_get(request: Request, path: str = Path(...)):
    return await proxy_request(settings.ORDER_SERVICE_URL, request)