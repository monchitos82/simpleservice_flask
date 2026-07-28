import datetime
import logging
import random
import string
import uuid

from flask import Blueprint, abort, current_app, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
from redis import RedisError

from schemas import RequestLogSchema
from models import RequestLog
from services import get_random
from utils import fibonacci, get_now_time

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

simplistic_bp = Blueprint("simplistic", __name__)
log = logging.getLogger(__name__)

REQUEST_COUNT = Counter("request_count", "Total Request Count", ["endpoint", "method"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency", ["endpoint"])


@simplistic_bp.route("/data", methods=["GET", "POST"])
def data() -> None:
    """Data endpoint returning a wrapped response from a downstream"""
    if request.method == "GET":
        try:
            return jsonify(
                {
                    "remote_random_data": get_random(
                        remote_url=current_app.config.get("REMOTE_RANDOM_URL")
                    )
                }
            )
        except (TypeError, ValueError, Exception) as error:
            log.error(f"Downstream call failed with error: {error}")
            abort(503)
    elif request.method == "POST":
        return jsonify(request.get_json())


@simplistic_bp.route("/errors", methods=["GET"])
def error() -> None:
    """Return a random HTTP error"""
    errors = [400, 401, 404, 419, 429, 500, 503]
    return "", random.choice(errors)


@simplistic_bp.route("/fibo/<int:number>", methods=["GET"])
def calculate(number: int) -> None:
    """Emit prometheus metrics for being scrapped"""
    if number < 10000:
        inserted = False
        if not hasattr(current_app, "redis_client"):
            return jsonify({"result": fibonacci(number), "status": "ok"})

        try:
            result = current_app.redis_client.get(number)
            if not result:
                result = fibonacci(number)
                current_app.redis_client.set(f"{number}", str(result))
                inserted = True
        except RedisError as error:
            log.error(f"Cache error: {error}")
            abort(500)
        else:
            if inserted:
                current_app.redis_client.persist(f"{number}")

        return jsonify({"result": int(result), "status": "ok"})
    abort(400)


@simplistic_bp.route("/metrics", methods=["GET"])
def metrics() -> None:
    """Emit prometheus metrics for being scrapped"""
    return generate_latest(), 200


@simplistic_bp.before_request
def start_timer() -> None:
    """Set the start time of a request"""
    request.start_time = get_now_time()


@simplistic_bp.after_request
def log_request(response) -> None:
    """Write the request details into the database"""
    latency = (get_now_time() - request.start_time).total_seconds()
    REQUEST_LATENCY.labels(request.endpoint).observe(latency)
    REQUEST_COUNT.labels(request.endpoint, request.method).inc()

    log.info(f"Request to {request.path} from {request.remote_addr}")
    # Log the request but don't store /metrics calls to avoid saturating the db
    try:
        if request.path in current_app.config.get("STORE_REQUEST_ENDPOINTS", ""):
            log_data = RequestLogSchema(
                ip_address=request.remote_addr,
                endpoint=request.path,
                method=request.method,
                response_code=response.status_code,
                timestamp=get_now_time(),
                scheme=request.scheme,
            )

            log_data_record = RequestLog(**log_data.model_dump(exclude={"id"}))

            current_app.db.session.add(log_data_record)
            current_app.db.session.commit()
    except (ValidationError, SQLAlchemyError) as error:
        log.error(f"Storing the request to {request.path} failed with error: {error}")
        abort(500)

    return response


@simplistic_bp.route("/random", methods=["GET"])
def get_random_json() -> None:
    fake = current_app.faker
    message = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(64)
    )
    return jsonify(
        {
            "timestamp": datetime.datetime.now().isoformat(),
            "id": str(uuid.uuid4()),
            "email": fake.email(),
            "score": round(random.uniform(0, 100), 2),
            "is_active": random.choice([True, False]),
            "message": message,
        }
    )
