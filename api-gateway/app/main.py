import httpx
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.core.models import UserCreate, Token, BookCreate, BookUpdate, OrderCreate
from app.core.config import settings

# Point to Gateway's login for the 'Authorize' button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app = FastAPI(
    title="Online Bookstore Gateway",
    description="Complete Entry Point for Auth, Book, and Order Services",
    version="1.0.0"
)

# --- PROXY ENGINE ---

async def proxy_request(target_url: str, request: Request, path: str, json_body: dict = None):
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)
    
    url = f"{target_url}/{path}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            if json_body:
                rp_resp = await client.request(request.method, url, headers=headers, json=json_body)
            else:
                rp_resp = await client.request(request.method, url, headers=headers, content=await request.body())
            return Response(content=rp_resp.content, status_code=rp_resp.status_code, headers=dict(rp_resp.headers))
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Service Error: {str(e)}")

# --- 1. AUTH SERVICE APIs ---

@app.post("/auth/register", tags=["Authentication"])
async def register(user_in: UserCreate, request: Request):
    """Register a new user account."""
    return await proxy_request(settings.AUTH_SERVICE_URL, request, "auth/register", json_body=user_in.model_dump())

@app.post("/auth/login", tags=["Authentication"], response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate and get a token."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{settings.AUTH_SERVICE_URL}/auth/login", 
                                 data={"username": form_data.username, "password": form_data.password})
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Invalid credentials")
        return resp.json()

# --- 2. BOOK SERVICE APIs ---

@app.get("/books/", tags=["Books"])
async def list_books(request: Request):
    """List all books with pagination."""
    return await proxy_request(settings.BOOK_SERVICE_URL, request, "books/")

@app.post("/books/", tags=["Books"], dependencies=[Depends(oauth2_scheme)])
async def create_book(book_in: BookCreate, request: Request):
    """Admin Only: Add a new book to inventory."""
    return await proxy_request(settings.BOOK_SERVICE_URL, request, "books/", json_body=book_in.model_dump())

@app.put("/books/{book_id}", tags=["Books"], dependencies=[Depends(oauth2_scheme)])
async def update_book(book_id: str, book_in: BookUpdate, request: Request):
    """Update book details or stock."""
    return await proxy_request(settings.BOOK_SERVICE_URL, request, f"books/{book_id}", json_body=book_in.model_dump(exclude_unset=True))

@app.delete("/books/{book_id}", tags=["Books"], dependencies=[Depends(oauth2_scheme)])
async def delete_book(book_id: str, request: Request):
    """Admin Only: Remove a book from inventory."""
    return await proxy_request(settings.BOOK_SERVICE_URL, request, f"books/{book_id}")  

# --- 3. ORDER SERVICE APIs ---

@app.post("/orders/", tags=["Orders"], dependencies=[Depends(oauth2_scheme)])
async def place_order(order_in: OrderCreate, request: Request):
    """Place an order and update inventory."""
    return await proxy_request(settings.ORDER_SERVICE_URL, request, "orders/", json_body=order_in.model_dump())

@app.get("/orders/my-orders", tags=["Orders"], dependencies=[Depends(oauth2_scheme)])
async def order_history(request: Request):
    """View personal order history."""
    return await proxy_request(settings.ORDER_SERVICE_URL, request, "orders/my-orders")

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
async def catch_all(service: str, path: str, request: Request):
    url_map = {"auth": settings.AUTH_SERVICE_URL, "books": settings.BOOK_SERVICE_URL, "orders": settings.ORDER_SERVICE_URL}
    if service not in url_map:
        raise HTTPException(status_code=404)
    return await proxy_request(url_map[service], request, f"{service}/{path}")