# REST API Development Fundamentals (PY-ADV-08)

This conceptual guide covers the foundational architectural principles, HTTP protocol specifics, status code taxonomy, and design patterns utilized in building scalable RESTful web APIs with Python and Flask.

---

## 🏛️ What is REST Architecture?

**REST** (**RE**presentational **S**tate **T**ransfer) is an architectural style defined by Roy Fielding in 2000 for designing networked applications. It relies on a stateless, client-server protocol—almost exclusively **HTTP**.

### Key Architectural Constraints of REST:

1. **Client-Server Separation**: The user interface (client) and data storage/business logic (server) are completely decoupled.
2. **Statelessness**: Every client request must contain all necessary information for the server to process it. The server stores no client session context between requests.
3. **Cacheability**: Responses must define themselves as cacheable or non-cacheable to prevent clients from reusing stale data.
4. **Uniform Interface**: Resources are uniquely identified using URIs (e.g. `/employees`), representations are transferred as JSON/XML, and messages are self-descriptive.
5. **Layered System**: Clients cannot tell whether they are connected directly to the end server or an intermediate proxy/load balancer.

---

## 🔄 HTTP Methods (Verbs) & Idempotency Matrix

| HTTP Method | CRUD Operation | Purpose | Safe? | Idempotent? |
| :--- | :--- | :--- | :---: | :---: |
| **GET** | Read | Retrieve resource representation(s) | Yes | Yes |
| **POST** | Create | Create a new resource under a collection | No | No |
| **PUT** | Update / Replace | Completely replace an existing resource | No | Yes |
| **PATCH** | Partial Update | Modify specific fields of a resource | No | No* |
| **DELETE** | Delete | Remove a resource by ID | No | Yes |

> **Idempotency Defined**: An operation is **idempotent** if making multiple identical requests has the same effect on the server state as making a single request.
> - `PUT /employees/1` with body `{"salary": 5000}` will set salary to 5000 regardless of how many times executed.
> - `POST /employees` creates a *new* employee record every time it is invoked, producing side effects.

---

## 🚦 HTTP Status Code Taxonomy

HTTP status codes inform the client of the outcome of their request.

### 1xx: Informational
- `100 Continue`: Server received initial request headers and client should proceed to send body.

### 2xx: Success
- **`200 OK`**: Request succeeded (Used for successful `GET`, `PUT`, `PATCH`, `DELETE`).
- **`201 Created`**: Resource successfully created (Used for `POST`). Accompanied by a `Location` header.
- **`204 No Content`**: Action succeeded, but no payload is returned in response body.

### 3xx: Redirection
- `301 Moved Permanently`: Resource URI has permanently shifted.
- `304 Not Modified`: Cached representation remains valid.

### 4xx: Client Errors
- **`400 Bad Request`**: Request payload failed schema validation, missing mandatory fields, or contains malformed JSON.
- **`401 Unauthorized`**: Authentication credentials are missing or invalid.
- **`403 Forbidden`**: Client is authenticated but lacks required authorization permissions.
- **`404 Not Found`**: Target URI or requested resource ID does not exist.
- **`405 Method Not Allowed`**: HTTP method is not supported for the requested route (e.g. `POST /employees/1`).
- **`409 Conflict`**: Conflict with target state (e.g., attempt to insert duplicate unique email).
- **`415 Unsupported Media Type`**: Missing or incorrect `Content-Type: application/json` header.
- **`422 Unprocessable Entity`**: Syntactically valid JSON containing semantic rule violations.

### 5xx: Server Errors
- **`500 Internal Server Error`**: Generic unhandled exception on the server.
- **`502 Bad Gateway`**: Upstream server returned invalid response to proxy.
- **`503 Service Unavailable`**: Server currently offline or overloaded.

---

## 🛡️ Request Validation & Error Handling Patterns

### Why Validate at the API Boundary?
1. **Security**: Prevents SQL injection, XSS, and corrupted state in data models.
2. **Predictability**: Guarantees strongly-typed inputs before hitting business logic.
3. **User Experience**: Returns clear, actionable validation error messages.

### Standardized Error Structure
A consistent error payload schema enables client applications to parse and display errors reliably:

```json
{
  "status": "error",
  "code": 400,
  "message": "Validation Error",
  "errors": {
    "email": "Invalid email address format",
    "salary": "Salary must be a non-negative number"
  },
  "timestamp": "2026-09-02T20:15:00Z"
}
```
