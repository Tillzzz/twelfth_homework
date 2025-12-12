import asyncio
import os

HTML_FILE_1 = "index.html"
HTML_FILE_2 = "index2.html"

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        # Читання даних від клієнта
        data = await reader.read(1024)
        message = data.decode()
        if not message:
            return
        # Отримання першого рядка запиту
        request_line = message.splitlines()[0]
        method, path, _ = request_line.split()  # розбиття по пробілам
        # Стандартна відповідь 404
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/plain\r\n"
            "\r\n"
            "Not Found"
        )

        #/page1
        if path == "/page1":
            if os.path.isfile(HTML_FILE_1):
                with open(HTML_FILE_1, "r", encoding="utf-8") as file:
                    html = file.read()
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(html.encode('utf-8'))}\r\n"
                    "\r\n"
                    f"{html}"
                )
        #/page2
        elif path == "/page2":
            if os.path.isfile(HTML_FILE_2):
                with open(HTML_FILE_2, "r", encoding="utf-8") as file:
                    html = file.read()
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(html.encode('utf-8'))}\r\n"
                    "\r\n"
                    f"{html}"
                )
        # Відправка відповіді
        writer.write(response.encode("utf-8"))
        await writer.drain()
    except Exception as e:
        print("Error handle client:", e)
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 9000)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
