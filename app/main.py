from flask import Flask
from app.apis.q_and_a import bp as q_and_a_bp


# DEVICE = "cpu"
# SOURCE = "context"
# N_RESULTS = 5
# COLLECTION_NAME = "All_Guideline_QA"  # "diabetes_qa"  # "diabetes_moh_guidelines"
# MODEL_NAME = "all-mpnet-base-v2"  # "all-MiniLM-L6-v2"
# ENV = dotenv.dotenv_values(".env")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or ENV["OPENAI_API_KEY"]
# openai.api_key = OPENAI_API_KEY


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(q_and_a_bp)
    return app


app = create_app()
