from .app import App


# --------------------
def main():
    app = App()
    app.init()
    app.run()
    app.term()


# --------------------
main()
