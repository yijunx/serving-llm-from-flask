up_sync_one:
	@echo "starting"
	@gunicorn app.main:app -w 1 -b 0.0.0.0:8000 --timeout 120

up_sync_three:
	@echo "starting"
	@gunicorn app.main:app -w 3 -b 0.0.0.0:8000 --timeout 120

up_sync_three_2_threads:
	@echo "starting"
	@gunicorn app.main:app -w 3 -b 0.0.0.0:8000 --timeout 120 --threads=2

up_async_one:
	@echo "starting gunicorn with worker gevent"
	@gunicorn app.patched:app --worker-class gevent -w 1 -b 0.0.0.0:8000 --timeout 120

up_async_three:
	@echo "starting gunicorn with worker gevent"
	@gunicorn app.patched:app --worker-class gevent -w 3 -b 0.0.0.0:8000 --timeout 120