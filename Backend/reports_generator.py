
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mijhar - Reports Generator
مولد التقارير لأداة Mijhar

Author: Hassan Mohamed Hassan Ahmed
GitHub: kush-king249
"""

import json
import os
from datetime import datetime
import hashlib

class ReportsGenerator:
    """مولد التقارير للتحليل الثابت والديناميكي"""
    
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """التأكد من وجود مجلد التقارير"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_combined_report(self, static_results, dynamic_results, output_format='html'):
        """إنشاء تقرير مدمج للتحليل الثابت والديناميكي"""
        try:
            report_id = self._generate_report_id()
            timestamp = datetime.now().isoformat()
            
            combined_data = {
                'report_id': report_id,
                'timestamp': timestamp,
                'static_analysis': static_results,
                'dynamic_analysis': dynamic_results,
                'summary': self._generate_summary(static_results, dynamic_results),
                'risk_assessment': self._assess_risk(static_results, dynamic_results)
            }
            
            if output_format == 'html':
                return self._generate_html_report(combined_data)
            elif output_format == 'json':
                return self._generate_json_report(combined_data)
            elif output_format == 'text':
                return self._generate_text_report(combined_data)
            else:
                raise ValueError(f"تنسيق غير مدعوم: {output_format}")
                
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_report_id(self):
        """إنشاء معرف فريد للتقرير"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_hash = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        return f"mijhar_{timestamp}_{random_hash}"
    
    def _generate_summary(self, static_results, dynamic_results):
        """إنشاء ملخص للتحليل"""
        summary = {
            'file_analyzed': static_results.get('file_path', 'غير محدد'),
            'analysis_timestamp': datetime.now().isoformat(),
            'static_analysis_completed': 'error' not in static_results,
            'dynamic_analysis_completed': 'error' not in dynamic_results,
            'key_findings': []
        }
        
        # إضافة النتائج الرئيسية من التحليل الثابت
        if 'suspicious_indicators' in static_results:
            indicators = static_results['suspicious_indicators']
            if indicators:
                summary['key_findings'].append(f"تم العثور على {len(indicators)} مؤشر مشبوه في التحليل الثابت")
        
        # إضافة النتائج الرئيسية من التحليل الديناميكي
        if 'changes_detected' in dynamic_results:
            changes = dynamic_results['changes_detected']
            if changes.get('network_activity_detected'):
                summary['key_findings'].append("تم اكتشاف نشاط شبكي أثناء التنفيذ")
            if changes.get('new_processes_created'):
                summary['key_findings'].append("تم إنشاء عمليات جديدة أثناء التنفيذ")
        
        return summary
    
    def _assess_risk(self, static_results, dynamic_results):
        """تقييم مستوى المخاطر"""
        risk_score = 0
        risk_factors = []
        
        # تقييم المخاطر من التحليل الثابت
        if 'suspicious_indicators' in static_results:
            indicators = static_results['suspicious_indicators']
            risk_score += len(indicators) * 10
            for indicator in indicators:
                risk_factors.append(f"مؤشر ثابت: {indicator.get('description', 'غير محدد')}")
        
        if 'entropy' in static_results:
            entropy = static_results['entropy']
            if entropy > 7.5:  # إنتروبيا عالية قد تشير للتشفير
                risk_score += 20
                risk_factors.append("إنتروبيا عالية - قد يكون الملف مشفراً")
        
        # تقييم المخاطر من التحليل الديناميكي
        if 'changes_detected' in dynamic_results:
            changes = dynamic_results['changes_detected']
            
            if changes.get('network_activity_detected'):
                risk_score += 30
                risk_factors.append("نشاط شبكي مكتشف")
            
            if changes.get('new_processes_created'):
                risk_score += 25
                risk_factors.append("إنشاء عمليات جديدة")
            
            suspicious_connections = changes.get('suspicious_network_connections', [])
            if suspicious_connections:
                risk_score += len(suspicious_connections) * 15
                risk_factors.append(f"{len(suspicious_connections)} اتصال شبكي مشبوه")
            
            suspicious_processes = changes.get('suspicious_processes', [])
            if suspicious_processes:
                risk_score += len(suspicious_processes) * 20
                risk_factors.append(f"{len(suspicious_processes)} عملية مشبوهة")
        
        # تحديد مستوى المخاطر
        if risk_score >= 80:
            risk_level = "عالي جداً"
            risk_color = "#dc3545"
        elif risk_score >= 60:
            risk_level = "عالي"
            risk_color = "#fd7e14"
        elif risk_score >= 40:
            risk_level = "متوسط"
            risk_color = "#ffc107"
        elif risk_score >= 20:
            risk_level = "منخفض"
            risk_color = "#20c997"
        else:
            risk_level = "آمن"
            risk_color = "#28a745"
        
        return {
            'score': risk_score,
            'level': risk_level,
            'color': risk_color,
            'factors': risk_factors
        }
    
    def _generate_html_report(self, data):
        """إنشاء تقرير HTML"""
        html_template = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير تحليل البرامج الضارة - Mijhar</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 30px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            overflow: hidden;
        }}
        .section-header {{
            background-color: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #e9ecef;
            font-weight: bold;
            font-size: 1.2em;
        }}
        .section-content {{
            padding: 20px;
        }}
        .risk-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            margin: 5px 0;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .info-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }}
        .info-card h4 {{
            margin: 0 0 10px 0;
            color: #007bff;
        }}
        .list-item {{
            background: #fff;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0;
        }}
        .hash-value {{
            font-family: 'Courier New', monospace;
            background: #f8f9fa;
            padding: 5px;
            border-radius: 3px;
            word-break: break-all;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            border-top: 1px solid #e9ecef;
            color: #6c757d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ تقرير تحليل البرامج الضارة</h1>
            <p>أداة Mijhar للتحليل الأمني المتقدم</p>
            <p>معرف التقرير: {report_id}</p>
        </div>
        
        <div class="content">
            <!-- ملخص التحليل -->
            <div class="section">
                <div class="section-header">📊 ملخص التحليل</div>
                <div class="section-content">
                    <div class="info-grid">
                        <div class="info-card">
                            <h4>الملف المحلل</h4>
                            <p>{file_path}</p>
                        </div>
                        <div class="info-card">
                            <h4>وقت التحليل</h4>
                            <p>{timestamp}</p>
                        </div>
                        <div class="info-card">
                            <h4>حالة التحليل</h4>
                            <p>ثابت: {static_status} | ديناميكي: {dynamic_status}</p>
                        </div>
                        <div class="info-card">
                            <h4>مستوى المخاطر</h4>
                            <span class="risk-badge" style="background-color: {risk_color}">
                                {risk_level} ({risk_score} نقطة)
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- عوامل المخاطر -->
            <div class="section">
                <div class="section-header">⚠️ عوامل المخاطر</div>
                <div class="section-content">
                    {risk_factors_html}
                </div>
            </div>
            
            <!-- التحليل الثابت -->
            <div class="section">
                <div class="section-header">🔍 نتائج التحليل الثابت</div>
                <div class="section-content">
                    {static_analysis_html}
                </div>
            </div>
            
            <!-- التحليل الديناميكي -->
            <div class="section">
                <div class="section-header">⚡ نتائج التحليل الديناميكي</div>
                <div class="section-content">
                    {dynamic_analysis_html}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>تم إنشاء هذا التقرير بواسطة أداة Mijhar</p>
            <p>المؤلف: Hassan Mohamed Hassan Ahmed | GitHub: kush-king249</p>
        </div>
    </div>
</body>
</html>
        """
        
        # تحضير البيانات للقالب
        summary = data['summary']
        risk = data['risk_assessment']
        
        # إنشاء HTML لعوامل المخاطر
        risk_factors_html = ""
        if risk['factors']:
            for factor in risk['factors']:
                risk_factors_html += f'<div class="list-item">• {factor}</div>'
        else:
            risk_factors_html = '<p>لم يتم اكتشاف عوامل مخاطر واضحة</p>'
        
        # إنشاء HTML للتحليل الثابت
        static_analysis_html = self._format_static_analysis_html(data['static_analysis'])
        
        # إنشاء HTML للتحليل الديناميكي
        dynamic_analysis_html = self._format_dynamic_analysis_html(data['dynamic_analysis'])
        
        # ملء القالب
        html_content = html_template.format(
            report_id=data['report_id'],
            file_path=summary['file_analyzed'],
            timestamp=summary['analysis_timestamp'],
            static_status="✅ مكتمل" if summary['static_analysis_completed'] else "❌ فشل",
            dynamic_status="✅ مكتمل" if summary['dynamic_analysis_completed'] else "❌ فشل",
            risk_level=risk['level'],
            risk_score=risk['score'],
            risk_color=risk['color'],
            risk_factors_html=risk_factors_html,
            static_analysis_html=static_analysis_html,
            dynamic_analysis_html=dynamic_analysis_html
        )
        
        # حفظ التقرير
        report_path = os.path.join(self.output_dir, f"{data['report_id']}.html")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return {
            'report_path': report_path,
            'report_id': data['report_id'],
            'format': 'html'
        }
    
    def _format_static_analysis_html(self, static_data):
        """تنسيق بيانات التحليل الثابت لـ HTML"""
        if 'error' in static_data:
            return f'<p style="color: red;">خطأ في التحليل: {static_data["error"]}</p>'
        
        html = ""
        
        # معلومات الملف
        if 'file_info' in static_data:
            file_info = static_data['file_info']
            html += f"""
            <div class="info-card">
                <h4>معلومات الملف</h4>
                <p><strong>الحجم:</strong> {file_info.get('size', 0):,} بايت</p>
                <p><strong>الامتداد:</strong> {file_info.get('extension', 'غير محدد')}</p>
            </div>
            """
        
        # الهاشات
        if 'hashes' in static_data:
            hashes = static_data['hashes']
            html += '<div class="info-card"><h4>الهاشات</h4>'
            for hash_type, hash_value in hashes.items():
                html += f'<p><strong>{hash_type.upper()}:</strong> <span class="hash-value">{hash_value}</span></p>'
            html += '</div>'
        
        # المؤشرات المشبوهة
        if 'suspicious_indicators' in static_data:
            indicators = static_data['suspicious_indicators']
            html += '<div class="info-card"><h4>المؤشرات المشبوهة</h4>'
            if indicators:
                for indicator in indicators:
                    html += f'<div class="list-item">• {indicator.get("description", "غير محدد")}</div>'
            else:
                html += '<p>لم يتم العثور على مؤشرات مشبوهة</p>'
            html += '</div>'
        
        return html
    
    def _format_dynamic_analysis_html(self, dynamic_data):
        """تنسيق بيانات التحليل الديناميكي لـ HTML"""
        if 'error' in dynamic_data:
            return f'<p style="color: red;">خطأ في التحليل: {dynamic_data["error"]}</p>'
        
        html = ""
        
        # نتائج التنفيذ
        if 'execution_results' in dynamic_data:
            exec_results = dynamic_data['execution_results']
            html += f"""
            <div class="info-card">
                <h4>نتائج التنفيذ</h4>
                <p><strong>كود الإرجاع:</strong> {exec_results.get('return_code', 'غير محدد')}</p>
                <p><strong>وقت التنفيذ:</strong> {exec_results.get('execution_time', 0):.2f} ثانية</p>
                <p><strong>انتهت المهلة الزمنية:</strong> {'نعم' if exec_results.get('timeout_occurred', False) else 'لا'}</p>
            </div>
            """
        
        # النشاط الشبكي
        if 'network_activity' in dynamic_data:
            network_activity = dynamic_data['network_activity']
            html += f'<div class="info-card"><h4>النشاط الشبكي ({len(network_activity)} اتصال)</h4>'
            if network_activity:
                for conn in network_activity[:10]:  # أول 10 اتصالات
                    html += f'<div class="list-item">{conn["local_address"]} → {conn["remote_address"]}</div>'
            else:
                html += '<p>لم يتم اكتشاف نشاط شبكي</p>'
            html += '</div>'
        
        # نشاط العمليات
        if 'process_activity' in dynamic_data:
            process_activity = dynamic_data['process_activity']
            html += f'<div class="info-card"><h4>العمليات الجديدة ({len(process_activity)} عملية)</h4>'
            if process_activity:
                for proc in process_activity[:10]:  # أول 10 عمليات
                    html += f'<div class="list-item">{proc["name"]} (PID: {proc["pid"]})</div>'
            else:
                html += '<p>لم يتم إنشاء عمليات جديدة</p>'
            html += '</div>'
        
        return html
    
    def _generate_json_report(self, data):
        """إنشاء تقرير JSON"""
        report_path = os.path.join(self.output_dir, f"{data['report_id']}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {
            'report_path': report_path,
            'report_id': data['report_id'],
            'format': 'json'
        }
    
    def _generate_text_report(self, data):
        """إنشاء تقرير نصي"""
        lines = []
        lines.append("=" * 80)
        lines.append("تقرير تحليل البرامج الضارة - أداة Mijhar")
        lines.append("=" * 80)
        lines.append(f"معرف التقرير: {data['report_id']}")
        lines.append(f"وقت الإنشاء: {data['timestamp']}")
        lines.append("")
        
        # ملخص التحليل
        summary = data['summary']
        lines.append("ملخص التحليل:")
        lines.append(f"  الملف: {summary['file_analyzed']}")
        lines.append(f"  التحليل الثابت: {'مكتمل' if summary['static_analysis_completed'] else 'فشل'}")
        lines.append(f"  التحليل الديناميكي: {'مكتمل' if summary['dynamic_analysis_completed'] else 'فشل'}")
        lines.append("")
        
        # تقييم المخاطر
        risk = data['risk_assessment']
        lines.append("تقييم المخاطر:")
        lines.append(f"  المستوى: {risk['level']} ({risk['score']} نقطة)")
        lines.append("  العوامل:")
        for factor in risk['factors']:
            lines.append(f"    - {factor}")
        lines.append("")
        
        # حفظ التقرير
        report_content = "\n".join(lines)
        report_path = os.path.join(self.output_dir, f"{data['report_id']}.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return {
            'report_path': report_path,
            'report_id': data['report_id'],
            'format': 'text'
        }

if __name__ == "__main__":
    # اختبار مولد التقارير
    generator = ReportsGenerator()
    print("مولد التقارير جاهز للاستخدام")
