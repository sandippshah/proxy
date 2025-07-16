from flask import Flask, request, Response
import cloudscraper

app = Flask(__name__)
scraper = cloudscraper.create_scraper()

BASE_URL = 'https://www.filmyzilla15.com'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    full_url = f"{BASE_URL}/{path}"
    if request.query_string:
        full_url += '?' + request.query_string.decode()

    try:
        print(f"🔁 Fetching: {full_url}")
        # Send GET request through cloudscraper
        res = scraper.get(full_url)

        # Optional: block troll page
        if 'Fuck You Bitch' in res.text:
            return Response('⚠️ Blocked by source site.', status=403)

        return Response(res.text, status=res.status_code, content_type=res.headers.get('Content-Type', 'text/html'))

    except Exception as e:
        print(f"❌ Error: {e}")
        return Response('Error fetching page.', status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
