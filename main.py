from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from urllib.parse import urlparse, parse_qs
import logging

# Создаем FastAPI приложение
app = FastAPI()

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"message": "Steam OpenID Callback Server"}

# Обработка Steam OpenID callback
@app.get("/steamcallback")
async def steam_callback(request: Request):
    # Получаем данные запроса
    query_params = urlparse(str(request.url)).query
    params = parse_qs(query_params)

    # Проверяем наличие 'openid.claimed_id' в параметрах
    if 'openid.claimed_id' not in params:
        logger.error("Ошибка аутентификации Steam. Не найден 'openid.claimed_id'.")
        raise HTTPException(status_code=400, detail="Invalid response from Steam")

    steam_id = params['openid.claimed_id'][0]
    logger.info(f"Получен Steam ID: {steam_id}")

    # Допустим, вы хотите выполнить запрос к Steam API для получения информации о пользователе.
    # Здесь можно интегрировать запрос к Steam API или хранить Steam ID для дальнейшей обработки.

    # Пример редиректа или ответа в зависимости от вашего приложения:
    # Если хотите редиректить в приложение, например на кастомную схему, используйте RedirectResponse:
    return RedirectResponse(url=f"myapp://steam?steamId={steam_id}")

    # Если хотите ответить с деталями:
    # return {"steam_id": steam_id, "message": "Authentication successful"}

# Запуск приложения с Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
