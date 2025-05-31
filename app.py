import os
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
import tempfile
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get video duration
        video = VideoFileClip(filepath)
        duration = video.duration
        video.close()
        
        return jsonify({
            'filename': filename,
            'duration': duration
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/split', methods=['POST'])
def split_video():
    data = request.json
    filename = data.get('filename')
    timestamps = data.get('timestamps', [])
    
    if not filename or not timestamps:
        return jsonify({'error': 'Missing filename or timestamps'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    # Create temporary directory for split videos
    temp_dir = tempfile.mkdtemp()
    split_files = []
    
    try:
        video = VideoFileClip(filepath)
        timestamps = [0] + timestamps + [video.duration]
        
        for i in range(len(timestamps) - 1):
            start_time = timestamps[i]
            end_time = timestamps[i + 1]
            
            # Extract subclip with audio
            subclip = video.subclip(start_time, end_time)
            

            output_path = os.path.join(temp_dir, f'part_{i+1}.mp4')
            subclip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',  # Use AAC codec for audio
                temp_audiofile=os.path.join(temp_dir, f'temp_audio_{i+1}.m4a'),
                remove_temp=True,
                threads=4,  # Use multiple threads for faster processing
                preset='medium'  # Balance between quality and speed
            )
            split_files.append(output_path)
        
        video.close()
        
        # Create a zip file containing all split videos
        zip_path = os.path.join(temp_dir, 'split_videos.zip')
        shutil.make_archive(zip_path[:-4], 'zip', temp_dir)
        
        return send_file(zip_path, as_attachment=True, download_name='split_videos.zip')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Cleanup
        for file in split_files:
            if os.path.exists(file):
                os.remove(file)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == '__main__':
    app.run(debug=True) 