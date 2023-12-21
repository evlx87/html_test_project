"""
Этот модуль определяет простой HTTP-сервер с использованием класса BaseHTTPRequestHandler.
Он обслуживает главную страницу и конкретное содержимое статьи на основе параметра запроса 'page'.

Использование:
    Запустите этот модуль, чтобы запустить HTTP-сервер.
    Перейдите по адресу http://localhost:8080 в веб-браузере.
    При необходимости добавьте параметр запроса 'page=news1',
    чтобы просмотреть конкретную статью.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from src.answers import ANSWER_1, ANSWER_2, ANSWER_3

HOST = "localhost"
PORT = 8080


class Server(BaseHTTPRequestHandler):

    def _get_index(self):
        """Читает и возвращает содержимое файла 'index.html'."""
        try:
            with open('index.html', encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return 'File not found'

    def _get_article_content(self, page_address):
        """Возвращает содержимое конкретной статьи на основе параметра page_address."""
        articles = {'news1': ANSWER_1, 'news2': ANSWER_2, 'news3': ANSWER_3}
        return articles.get(page_address, 'Article not found!')

    def do_GET(self):
        """Обрабатывает запросы GET, разбирает параметры запроса
        и обслуживает соответствующее содержимое."""
        query_components = parse_qs(urlparse(self.path).query)
        page_address = query_components.get('page')
        page_content = self._get_index()
        if page_address:
            page_content = self._get_article_content(page_address[0])
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page_content, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((HOST, PORT), Server)
    print(f"Сервер запущен - http://{HOST}:{PORT}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Работа сервера остановлена.")
