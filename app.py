from flask import Flask, request, render_template, jsonify, redirect, url_for
import base64
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-pass', methods=['POST'])
def generate_pass():
    name = request.form.get('name')
    validity = request.form.get('validity')
    start_date = request.form.get('startDate')
    pass_no = request.form.get('passNo')
    profile_pic = request.files.get('profilePic')

    if not name or not validity or not start_date or not pass_no:
        return jsonify({'error': 'Please fill in all required fields'}), 400

    # Convert the profile picture to base64
    profile_pic_base64 = ''
    if profile_pic:
        profile_pic_bytes = profile_pic.read()
        profile_pic_base64 = base64.b64encode(profile_pic_bytes).decode('utf-8')

    response_data = {
        'name': name,
        'validity': validity,
        'startDate': start_date,
        'passNo': pass_no,
        'profilePicBase64': profile_pic_base64
    }
    return jsonify(response_data)

@app.route('/bus-pass')
def bus_pass():
    # Extract query parameters
    name = request.args.get('name')
    validity = request.args.get('validity')
    start_date = request.args.get('startDate')
    pass_no = request.args.get('passNo')
    profile_pic_base64 = request.args.get('profilePicBase64')

    return render_template('bus-pass.html', name=name, validity=validity, start_date=start_date,
                           pass_no=pass_no, profile_pic_base64=profile_pic_base64)

# if __name__ == '__main__':
#     app.run(port=3000, debug=True)

if __name__ == '__main__':
    # Use the port and host recommended by Render
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
