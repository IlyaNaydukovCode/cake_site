# run_websocket.py
import uvicorn
import signal
import sys

def run_server():
    """Запуск сервера с WebSocket чатом"""
    print("=" * 60)
    print("🚀 Cake Site WebSocket Chat Server")
    print("=" * 60)
    print()
    print("📡 WebSocket endpoint: ws://localhost:8000/ws/chat")
    print("🔗 HTTP API:          http://localhost:8000")
    print("🧪 Тестовая страница: http://localhost:8000/test_chat.html")
    print()
    print("👥 Для тестирования:")
    print("   1. Откройте тестовую страницу в двух вкладках браузера")
    print("   2. Авторизуйтесь под разными пользователями")
    print("   3. Отправляйте сообщения и проверяйте их получение")
    print()
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    run_server()