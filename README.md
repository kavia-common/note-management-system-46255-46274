# note-management-system-46255-46274

Notes App Backend (Django + DRF)

Base URL
- Docs: /docs
- API: /api

Health
- GET /api/health
  - 200 {"message": "Server is up!"}

Auth (Token)
- POST /api/auth/register
  Body: {"username":"alice","password":"SuperSecret123!"}
  201 {"user":{"id":1,"username":"alice"},"token":"<token>"}

- POST /api/auth/login
  Body: {"username":"alice","password":"SuperSecret123!"}
  200 {"user":{"id":1,"username":"alice"},"token":"<token>"}

Notes (Authenticated - Token header: Authorization: Token <token>)
- GET /api/notes?page=1&page_size=10&q=search
- POST /api/notes
  {"title":"Meeting Notes","content":"Action items..."}

- GET /api/notes/{id}
- PUT /api/notes/{id}
  {"title":"Updated","content":"Revised content"}
- PATCH /api/notes/{id}
  {"title":"Partially updated"}
- DELETE /api/notes/{id}

Curl examples:
- Register:
  curl -s -X POST http://localhost:3001/api/auth/register -H "Content-Type: application/json" -d '{"username":"alice","password":"SuperSecret123!"}'

- Login:
  curl -s -X POST http://localhost:3001/api/auth/login -H "Content-Type: application/json" -d '{"username":"alice","password":"SuperSecret123!"}'

- Create note:
  curl -s -X POST http://localhost:3001/api/notes/ -H "Authorization: Token <token>" -H "Content-Type: application/json" -d '{"title":"Test","content":"Body"}'

- List notes:
  curl -s -X GET "http://localhost:3001/api/notes/?page=1&page_size=10&q=test" -H "Authorization: Token <token>"

Environment variables (.env.example):
- DJANGO_DEBUG=true
- DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,.kavia.ai
- CORS_ALLOW_ALL=true

Notes:
- Uses SQLite for local/dev.
- Token auth via DRF TokenAuthentication.
- CORS enabled for local development.
