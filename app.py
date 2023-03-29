import os
from flask import Flask, render_template, send_from_directory, request, make_response, send_file
import zipfile



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Function to process uploaded images and return results
        results = request.files.getlist('images')
        # Function to save results to files and return filenames
        result_filenames = save_results(results)
        # Function to create a zip file containing the result files and return its filename
        zip_filename = create_zip(result_filenames)
        # Function to send the zip file for download
        return send_download(zip_filename)
    return render_template('index.html')


@app.route('/download/<path:filename>')
def download_file(filename):
    """Flask route to serve static files"""
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


def save_results(results):
    """Function to save results and return filenames"""
    result_filenames = []
    for i, result in enumerate(results):
        filename = f"result_{i}.jpg"
        result.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        result_filenames.append(filename)
    return result_filenames


def create_zip(filenames):
    """Function to create a zip file and return its filename"""
    zip_filename = 'results.zip'
    with zipfile.ZipFile(os.path.join(app.config['DOWNLOAD_FOLDER'], zip_filename), 'w') as zip:
        for filename in filenames:
            zip.write(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
    return zip_filename


def send_download(filename):
    """Function to send the download response"""
    response = make_response(send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_attachment=True))
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.headers['Content-Type'] = 'application/zip'
    return response



if __name__ == "__main__":
    app.run(debug=True)