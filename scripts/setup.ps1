# Setup Script for Windows PowerShell

Write-Host "Setting up EchoCrew Environment..." -ForegroundColor Green

if (-Not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example" -ForegroundColor Yellow
}

if (-Not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "Created Python virtual environment .venv" -ForegroundColor Yellow
}

Write-Host "Setup complete!" -ForegroundColor Green
