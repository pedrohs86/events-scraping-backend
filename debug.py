from src import server

if __name__ == "__main__":
    server.run(
        host="0.0.0.0",
        port=8000,
        debug=True, 
        use_debugger=True, 
        use_reloader=True,
        )