# ⚖️ HATVP RAG API 📝

Welcome to the HATVP RAG API! This project provides a Flask API to showcase the inference capabilities of our RAG (Retrieval-Augmented Generation) system using various datasets.

📌 **Repository URL**: [https://github.com/louispaulet/hatvp_rag_api](https://github.com/louispaulet/hatvp_rag_api)

## 🚀 Getting Started

### Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/louispaulet/hatvp_rag_api.git
    cd hatvp_rag_api
    ```

2. Create a `.env` file in the root directory and add your API keys:
    ```
    OPENAI_API_KEY=your_openai_api_key
    GROQ_API_KEY=your_groq_api_key
    ```

3. Build and run the Docker container using Docker Compose:
    ```sh
    docker-compose up --build
    ```

### Usage

The Flask application will be accessible at `http://localhost:5000`. You can make a POST request to `http://localhost:5000/ask` with a JSON payload containing your question:

```json
{
    "question": "Quel est le salaire de Damien Abad en 2019?"
}
```

### Example

To ask a question, use the following curl command:

```sh
  curl 'http://127.0.0.1:5000/ask' \
  -H 'Accept: */*' \
  -H 'Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Origin: http://localhost:3000' \
  -H 'Pragma: no-cache' \
  -H 'Referer: http://localhost:3000/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --data-raw '{"question":"who is maire of paris? what is the salary?"}'
```

## 📂 Project Structure

- `main.py`: Contains the Flask application code.
- `Dockerfile`: Instructions to build the Docker image.
- `docker-compose.yml`: Configuration for Docker Compose.
- `requirements.txt`: List of Python dependencies.


## ✨ Contributing

We welcome contributions! 

Enjoy using the HATVP RAG API! 🎉