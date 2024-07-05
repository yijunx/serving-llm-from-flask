def get_patched_app():
    from gevent import monkey

    monkey.patch_all()  # gevent patch to support implicit asynchronous

    from app.main import app

    return app

# to enable gRPC!
# def get_patched_app():


#     from gevent import monkey
#     monkey.patch_all()

#     import grpc._cython.cygrpc
#     grpc._cython.cygrpc.init_grpc_gevent()

#     from app.websocket_app import app

#     return app


# app = get_patched_app()


app = get_patched_app()
