from fastapi import FastAPI
import uvicorn
from infrastructure.config.settings import settings
from infrastructure.http.cors import setup_cors
from presentation.routes.api_router import create_api_router


# Cria a instância do FastAPI
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)

# Configuração de CORS
setup_cors(app)

# Registra as rotas da API
api_router = create_api_router()
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
