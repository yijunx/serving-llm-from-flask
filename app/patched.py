def get_patched_app():
    from gevent import monkey

    monkey.patch_all()  # gevent patch to support implicit asynchronous

    from app.main import app

    return app


app = get_patched_app()
