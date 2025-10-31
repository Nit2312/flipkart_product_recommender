from flask import render_template, Flask, request, Response
from prometheus_client import Counter, generate_latest

from flipkart.data_ingestion import DataIngestor
from flipkart.rag_chain import RAGChainBuilder

from dotenv import load_dotenv
load_dotenv()

REQUEST_COUNT = Counter("http_requests_total", "Total_HTTP Requests") # Custom Matrix
ANSWER_INFO = Counter("answer_request_total", "Total_chat_requests")



def create_app():
    app = Flask(__name__)
    
    vectorstore = DataIngestor().ingest(load_existing=True)
    rag_chain = RAGChainBuilder(vectorstore).build_chain()
    
    @app.route("/")
    def index():
        REQUEST_COUNT.inc()
        return render_template("index.html")
    
    @app.route("/get", methods=["POST"])
    def get_response():
        ANSWER_INFO.inc()
        user_input = request.form["msg"]
        Response = rag_chain.invoke(
                {"input": user_input},
                config = {"configurable": {"session_id" : "user-session"}}
        )["answer"]
        
        return Response
    
    @app.route("/metrices")
    def metrics():
        res = Response(generate_latest(), mimetype="text/plain") # inbuilt matrices suported by 
        return res
        
    return app
    
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
    
    