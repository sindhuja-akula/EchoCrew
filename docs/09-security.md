# 09 - Security & Compliance 🛡️

## Security Guidelines
- **Authentication**: JWT tokens with HMAC-SHA256 signatures.
- **Password Hashing**: Passwords stored using bcrypt hashing algorithm.
- **CORS Policy**: Strict origin checks configured via environment settings.
- **Secret Management**: Sensitive keys loaded exclusively via environment variables (`.env`).
