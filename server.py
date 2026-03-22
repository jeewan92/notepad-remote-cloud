from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA = {
    "html": "",
    "reply": "",
    "updated_at": 0,
}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/send")
async def send_content(html: str = Form(...)):
    DATA["html"] = html
    DATA["updated_at"] = int(time.time())
    return {"status": "ok"}

@app.post("/reply")
async def save_reply(reply: str = Form(...)):
    DATA["reply"] = reply
    DATA["updated_at"] = int(time.time())
    return {"status": "ok"}

@app.get("/latest")
def latest():
    return {
        "html": DATA["html"],
        "reply": DATA["reply"],
        "updated_at": DATA["updated_at"],
    }

@app.get("/", response_class=HTMLResponse)
def phone_page():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Remote Note</title>
    <style>
        body {
            margin: 0;
            padding: 16px;
            font-family: Arial, sans-serif;
            background: #f3f3f3;
        }
        .card {
            background: #fff;
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 14px;
            box-shadow: 0 1px 6px rgba(0,0,0,0.08);
        }
        .title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .content {
            min-height: 80px;
            overflow-wrap: break-word;
        }
        .content img {
            max-width: 100%;
            height: auto;
            display: block;
            margin-top: 8px;
            border-radius: 6px;
        }
        input, button {
            width: 100%;
            box-sizing: border-box;
            padding: 12px;
            font-size: 16px;
            margin-top: 8px;
        }
        button {
            cursor: pointer;
        }
        .small {
            color: #666;
            font-size: 12px;
            margin-top: 8px;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="title">Latest Content</div>
        <div id="content" class="content"></div>
        <div id="updated" class="small"></div>
    </div>

    <div class="card">
        <div class="title">Reply</div>
        <input id="replyInput" type="text" placeholder="Type your reply">
        <button onclick="sendReply()">Send Reply</button>
    </div>

    <script>
        let lastHtml = "";

        async function loadLatest() {
            try {
                const res = await fetch('/latest?ts=' + Date.now(), { cache: 'no-store' });
                const data = await res.json();

                if ((data.html || "") !== lastHtml) {
                    document.getElementById('content').innerHTML = data.html || "";
                    lastHtml = data.html || "";
                }

                if (data.updated_at) {
                    document.getElementById('updated').textContent =
                        "Updated: " + new Date(data.updated_at * 1000).toLocaleString();
                }
            } catch (err) {
                console.log(err);
            }
        }

        async function sendReply() {
            const input = document.getElementById('replyInput');
            const value = input.value.trim();
            if (!value) return;

            const body = new URLSearchParams();
            body.append('reply', value);

            const res = await fetch('/reply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: body.toString()
            });

            if (res.ok) {
                input.value = "";
                alert("Reply sent");
            } else {
                alert("Failed to send reply");
            }
        }

        loadLatest();
        setInterval(loadLatest, 2000);
    </script>
</body>
</html>
    """
