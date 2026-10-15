from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, uuid
from process import process_image

UPLOAD_DIR = "data/uploads"
OUT_DIR = "data/out"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)  # allow widget served from file/http to call this backend

@app.route('/process', methods=['POST'])
def process():
    f = request.files.get('image')
    sku = request.form.get('sku') or str(uuid.uuid4())[:8]
    if not f:
        return jsonify({"error":"no file"}), 400
    fname = f"{sku}_{uuid.uuid4().hex[:8]}.png"
    in_path = os.path.join(UPLOAD_DIR, fname)
    f.save(in_path)
    try:
        out_path, report_path = process_image(in_path, OUT_DIR, sku=sku)
        base = f"http://localhost:43218/files"
        return jsonify({"output_url": f"{base}/{os.path.basename(out_path)}", "report_url": f"{base}/{os.path.basename(report_path)}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files/<path:fn>')
def files(fn):
    return send_from_directory(OUT_DIR, fn)

if __name__ == '__main__':
    print("Starting backend on http://localhost:43218")
    app.run(port=43218, host='0.0.0.0', debug=False)
