import httpx
from typing import Any, Optional
from fastapi import FastAPI, Request, Response, HTTPException, Path, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# 1. Define the OAuth2 scheme so the 'Authorize' button appears in Swagger
# tokenUrl points to the Gateway's login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

app = FastAPI(
    title="API Gateway",
    description="Unified Entry Point for Tharun's Microservices",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

async def proxy_request(target_url: str, request: Request, service_prefix: str):
    """
    Transparent Proxy Handler:
    Handles JSON/Form payloads and buffers responses to prevent 'null' outputs.
    """
    body_content = await request.body()
    headers = dict(request.headers)
    
    # Clean headers for internal Docker network hops
    headers.pop("host", None)
    headers.pop("content-length", None)

    # Path Reconstruction (Removes double slashes)
    path_param = request.path_params.get("path", "").strip("/")
    full_path = f"{service_prefix}/{path_param}" if path_param else f"{service_prefix}/"
    url = f"{target_url}/{full_path}"
    
    if request.query_params:
        url += f"?{request.query_params}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            rp_req = client.build_request(
                request.method,
                url,
                headers=headers,
                content=body_content
            )
            rp_resp = await client.send(rp_req)
            response_content = await rp_resp.aread() # Ensures full data is read
            
            return Response(
                content=response_content,
                status_code=rp_resp.status_code,
                headers=dict(rp_resp.headers)
            )
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Gateway Error: {str(e)}")

# --- SYSTEM ROUTES ---

@app.get("/health", tags=["System"])
async def health():
    return {"status": "Gateway Online", "architecture": "Microservices"}

# --- MICROSERVICE PROXIES ---

# 1. AUTH SERVICE (Login, Register, User Management)
@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], tags=["Auth"])
async def auth_proxy(request: Request, path: Optional[str] = ""):
    return await proxy_request(settings.AUTH_SERVICE_URL, request, "auth")

# 2. BOOK SERVICE (Inventory Management) - PROTECTED
@app.api_route(
    "/books/{path:path}", 
    methods=["GET", "POST", "PUT", "DELETE"], 
    tags=["Books"],
    dependencies=[Depends(oauth2_scheme)]
)
async def books_proxy(request: Request, path: Optional[str] = ""):
    return await proxy_request(settings.BOOK_SERVICE_URL, request, "books")

# 3. ORDER SERVICE (Checkout, Transaction History) - PROTECTED
@app.api_route(
    "/orders/{path:path}", 
    methods=["GET", "POST", "PUT", "DELETE"], 
    tags=["Orders"],
    dependencies=[Depends(oauth2_scheme)]
)
async def orders_proxy(request: Request, path: Optional[str] = ""):
    return await proxy_request(settings.ORDER_SERVICE_URL, request, "orders")