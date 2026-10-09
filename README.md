# SecureCart AI — Python Commerce API Demo

A Python FastAPI backend application demonstrating RESTful API development, e-commerce business logic, input validation, and automated testing.

The application provides product inventory management, shopping cart functionality, stock validation, order creation, and checkout confirmation, along with an optional asynchronous Claude API integration.

## Technology Stack

- **Backend:** Python, FastAPI
- **API Development:** RESTful APIs, Pydantic
- **AI Integration:** Anthropic Claude API (optional)
- **Testing:** Pytest
- **API Documentation:** Swagger UI / OpenAPI
- **Data Storage:** In-memory storage for demonstration

## Implemented Features

- Product listing and inventory tracking
- Shopping cart management
- Stock availability validation
- Checkout with explicit user confirmation
- Order creation and management
- Request validation and API error handling
- Automated API testing with pytest
- Interactive API documentation

## Run on Windows

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs and test `GET /products`.

## Run Automated Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Optional Claude Integration

Set `ANTHROPIC_API_KEY` in your terminal environment before starting the server.

The `/assistant` endpoint sends user messages to Claude asynchronously. It does not currently perform agent tool calling or execute checkout operations.

## Planned Enhancements

- MCP server using Streamable HTTP
- Claude agent with tool calling
- OAuth 2.0 authentication and JWT/JWKS validation
- PostgreSQL database persistence
- Asynchronous external e-commerce API integrations

## Scope and Limitations

This is an **in-memory portfolio demonstration**, not a production commerce platform.

- No real payments are processed.
- Inventory and orders reset when the server restarts.
- Production authentication and authorization are not implemented.
- Do not deploy publicly or use real customer data.