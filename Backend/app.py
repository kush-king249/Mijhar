
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mijhar - Flask Backend Application
تطبيق Flask للواجهة الخلفية لأداة Mijhar

Author: Hassan Mohamed Hassan Ahmed
GitHub: kush-king249
"""

from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import os
import tempfile
import threading
from werkzeug.utils import secure_filename
from static_analyzer import StaticAnalyzer
from dynamic_analyzer import DynamicAnalyzer
from reports_generator import ReportsGenerator

app = Flask(__name__)
CORS(app)

# إعدادات التطبيق
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

# إنشاء مجلد التحميل إذا لم يكن موجوداً
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# إنشاء كائنات المحللات
static_analyzer = StaticAnalyzer()
dynamic_analyzer = DynamicAnalyzer()
reports_generator = ReportsGenerator()

# قاموس لتخزين حالة التحليل
analysis_status = {}

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template_string("""
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mijhar - أداة تحليل البرامج الضارة</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            max-width: 800px;
            width: 90%;
        }
        
        .logo {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.2em;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        
        .upload-area {
            border: 2px dashed rgba(255, 255, 255, 0.5);
            border-radius: 15px;
            padding: 40px;
            margin: 30px 0;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .upload-area:hover {
            border-color: rgba(255, 255, 255, 0.8);
            background: rgba(255, 255, 255, 0.1);
        }
        
        .upload-area.dragover {
            border-color: #4CAF50;
            background: rgba(76, 175, 80, 0.2);
        }
        
        .upload-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        
        .upload-text {
            font-size: 1.1em;
            margin-bottom: 15px;
        }
        
        .file-input {
            display: none;
        }
        
        .btn {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
            margin: 10px;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .btn-primary {
            background: #4CAF50;
            border-color: #4CAF50;
        }
        
        .btn-primary:hover {
            background: #45a049;
        }
        
        .analysis-options {
            margin: 20px 0;
        }
        
        .checkbox-group {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 20px 0;
        }
        
        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .checkbox-item input[type="checkbox"] {
            width: 20px;
            height: 20px;
        }
        
        .progress-container {
            display: none;
            margin: 20px 0;
        }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: #4CAF50;
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .status-text {
            margin-top: 10px;
            font-size: 1.1em;
        }
        
        .results-container {
            display: none;
            margin-top: 30px;
            text-align: right;
        }
        
        .result-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
        }
        
        .result-title {
            font-size: 1.3em;
            margin-bottom: 15px;
            color: #4CAF50;
        }
        
        .footer {
            margin-top: 40px;
            font-size: 0.9em;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🛡️</div>
        <h1>Mijhar</h1>
        <p class="subtitle">أداة تحليل البرامج الضارة المتقدمة</p>
        
        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">📁</div>
            <div class="upload-text">اسحب وأفلت الملف هنا أو انقر للاختيار</div>
            <input type="file" id="fileInput" class="file-input" accept=".exe,.dll,.bin">
            <button class="btn" onclick="document.getElementById('fileInput').click()">اختيار ملف</button>
        </div>
        
        <div class="analysis-options">
            <div class="checkbox-group">
                <div class="checkbox-item">
                    <input type="checkbox" id="staticAnalysis" checked>
                    <label for="staticAnalysis">التحليل الثابت</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="dynamicAnalysis" checked>
                    <label for="dynamicAnalysis">التحليل الديناميكي</label>
                </div>
            </div>
            <button class="btn btn-primary" id="analyzeBtn" onclick="startAnalysis()" disabled>بدء التحليل</button>
        </div>
        
        <div class="progress-container" id="progressContainer">
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="status-text" id="statusText">جاري التحليل...</div>
        </div>
        
        <div class="results-container" id="resultsContainer">
            <div class="result-section">
                <div class="result-title">نتائج التحليل</div>
                <div id="resultsContent"></div>
            </div>
            <button class="btn" id="downloadBtn" onclick="downloadReport()">تحميل التقرير</button>
        </div>
        
        <div class="footer">
            <p>تم تطوير هذه الأداة بواسطة Hassan Mohamed Hassan Ahmed</p>
            <p>GitHub: kush-king249</p>
        </div>
    </div>

    <script>
        let selectedFile = null;
        let analysisId = null;
        
        // إعداد منطقة السحب والإفلات
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const analyzeBtn = document.getElementById('analyzeBtn');
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelect(files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0]);
            }
        });
        
        function handleFileSelect(file) {
            selectedFile = file;
            document.querySelector('.upload-text').textContent = `تم اختيار: ${file.name}`;
            analyzeBtn.disabled = false;
        }
        
        async function startAnalysis() {
            if (!selectedFile) return;
            
            const staticAnalysis = document.getElementById('staticAnalysis').checked;
            const dynamicAnalysis = document.getElementById('dynamicAnalysis').checked;
            
            if (!staticAnalysis && !dynamicAnalysis) {
                alert('يرجى اختيار نوع تحليل واحد على الأقل');
                return;
            }
            
            // إظهار شريط التقدم
            document.getElementById('progressContainer').style.display = 'block';
            document.getElementById('resultsContainer').style.display = 'none';
            analyzeBtn.disabled = true;
            
            // رفع الملف
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('static_analysis', staticAnalysis);
            formData.append('dynamic_analysis', dynamicAnalysis);
            
            try {
                updateProgress(10, 'رفع الملف...');
                
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.error) {
                    throw new Error(result.error);
                }
                
                analysisId = result.analysis_id;
                pollAnalysisStatus();
                
            } catch (error) {
                alert('خطأ في التحليل: ' + error.message);
                resetUI();
            }
        }
        
        async function pollAnalysisStatus() {
            try {
                const response = await fetch(`/api/status/${analysisId}`);
                const status = await response.json();
                
                updateProgress(status.progress, status.message);
                
                if (status.completed) {
                    displayResults(status.results);
                } else {
                    setTimeout(pollAnalysisStatus, 1000);
                }
                
            } catch (error) {
                alert('خطأ في متابعة التحليل: ' + error.message);
                resetUI();
            }
        }
        
        function updateProgress(percent, message) {
            document.getElementById('progressFill').style.width = percent + '%';
            document.getElementById('statusText').textContent = message;
        }
        
        function displayResults(results) {
            document.getElementById('progressContainer').style.display = 'none';
            document.getElementById('resultsContainer').style.display = 'block';
            
            const resultsContent = document.getElementById('resultsContent');
            let html = '';
            
            if (results.static_analysis) {
                html += '<h4>التحليل الثابت:</h4>';
                html += `<p>الهاشات: ${Object.keys(results.static_analysis.hashes || {}).length}</p>`;
                html += `<p>المؤشرات المشبوهة: ${(results.static_analysis.suspicious_indicators || []).length}</p>`;
            }
            
            if (results.dynamic_analysis) {
                html += '<h4>التحليل الديناميكي:</h4>';
                html += `<p>النشاط الشبكي: ${(results.dynamic_analysis.network_activity || []).length} اتصال</p>`;
                html += `<p>العمليات الجديدة: ${(results.dynamic_analysis.process_activity || []).length} عملية</p>`;
            }
            
            if (results.risk_assessment) {
                html += '<h4>تقييم المخاطر:</h4>';
                html += `<p style="color: ${results.risk_assessment.color}">المستوى: ${results.risk_assessment.level}</p>`;
                html += `<p>النقاط: ${results.risk_assessment.score}</p>`;
            }
            
            resultsContent.innerHTML = html;
            analyzeBtn.disabled = false;
        }
        
        async function downloadReport() {
            if (!analysisId) return;
            
            try {
                const response = await fetch(`/api/report/${analysisId}`);
                const blob = await response.blob();
                
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `mijhar_report_${analysisId}.html`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
            } catch (error) {
                alert('خطأ في تحميل التقرير: ' + error.message);
            }
        }
        
        function resetUI() {
            document.getElementById('progressContainer').style.display = 'none';
            document.getElementById('resultsContainer').style.display = 'none';
            analyzeBtn.disabled = false;
        }
    </script>
</body>
</html>
    """)

@app.route('/api/analyze', methods=['POST'])
def analyze_file():
    """تحليل ملف مرفوع"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'لم يتم رفع ملف'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'لم يتم اختيار ملف'}), 400
        
        # حفظ الملف
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # إنشاء معرف التحليل
        analysis_id = f"analysis_{len(analysis_status)}"
        
        # إعداد حالة التحليل
        analysis_status[analysis_id] = {
            'progress': 0,
            'message': 'بدء التحليل...',
            'completed': False,
            'results': None,
            'file_path': file_path
        }
        
        # بدء التحليل في خيط منفصل
        static_analysis = request.form.get('static_analysis') == 'true'
        dynamic_analysis = request.form.get('dynamic_analysis') == 'true'
        
        thread = threading.Thread(
            target=perform_analysis,
            args=(analysis_id, file_path, static_analysis, dynamic_analysis)
        )
        thread.start()
        
        return jsonify({'analysis_id': analysis_id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def perform_analysis(analysis_id, file_path, static_analysis, dynamic_analysis):
    """تنفيذ التحليل في خيط منفصل"""
    try:
        results = {}
        
        # التحليل الثابت
        if static_analysis:
            analysis_status[analysis_id]['progress'] = 20
            analysis_status[analysis_id]['message'] = 'جاري التحليل الثابت...'
            
            static_results = static_analyzer.analyze_file(file_path)
            results['static_analysis'] = static_results
            
            analysis_status[analysis_id]['progress'] = 50
        
        # التحليل الديناميكي
        if dynamic_analysis:
            analysis_status[analysis_id]['progress'] = 60
            analysis_status[analysis_id]['message'] = 'جاري التحليل الديناميكي...'
            
            dynamic_results = dynamic_analyzer.analyze_file(file_path, timeout=30)
            results['dynamic_analysis'] = dynamic_results
            
            analysis_status[analysis_id]['progress'] = 80
        
        # إنشاء التقرير
        analysis_status[analysis_id]['progress'] = 90
        analysis_status[analysis_id]['message'] = 'إنشاء التقرير...'
        
        static_results = results.get('static_analysis', {})
        dynamic_results = results.get('dynamic_analysis', {})
        
        report_result = reports_generator.generate_combined_report(
            static_results, dynamic_results, 'html'
        )
        
        results['report'] = report_result
        results['risk_assessment'] = reports_generator._assess_risk(static_results, dynamic_results)
        
        # إكمال التحليل
        analysis_status[analysis_id]['progress'] = 100
        analysis_status[analysis_id]['message'] = 'تم إكمال التحليل'
        analysis_status[analysis_id]['completed'] = True
        analysis_status[analysis_id]['results'] = results
        
    except Exception as e:
        analysis_status[analysis_id]['message'] = f'خطأ في التحليل: {str(e)}'
        analysis_status[analysis_id]['completed'] = True

@app.route('/api/status/<analysis_id>')
def get_analysis_status(analysis_id):
    """الحصول على حالة التحليل"""
    if analysis_id not in analysis_status:
        return jsonify({'error': 'معرف التحليل غير موجود'}), 404
    
    return jsonify(analysis_status[analysis_id])

@app.route('/api/report/<analysis_id>')
def download_report(analysis_id):
    """تحميل التقرير"""
    if analysis_id not in analysis_status:
        return jsonify({'error': 'معرف التحليل غير موجود'}), 404
    
    status = analysis_status[analysis_id]
    if not status['completed'] or not status['results']:
        return jsonify({'error': 'التحليل لم يكتمل بعد'}), 400
    
    report_info = status['results'].get('report')
    if not report_info or 'report_path' not in report_info:
        return jsonify({'error': 'التقرير غير متوفر'}), 404
    
    return send_file(
        report_info['report_path'],
        as_attachment=True,
        download_name=f"mijhar_report_{analysis_id}.html"
    )

@app.route('/health')
def health_check():
    """فحص صحة التطبيق"""
    return jsonify({
        'status': 'healthy',
        'service': 'Mijhar Analysis API',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🛡️ بدء تشغيل خادم Mijhar...")
    print("📍 الواجهة متاحة على: http://localhost:5000")
    print("🔗 API متاح على: http://localhost:5000/api/")
    app.run(debug=True, host='0.0.0.0', port=5000)
