
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mijhar - Dynamic Analysis Engine
محرك التحليل الديناميكي لأداة Mijhar

Author: Hassan Mohamed Hassan Ahmed
GitHub: kush-king249
"""

import psutil
import subprocess
import threading
import time
import json
import os
from datetime import datetime
import socket
import re

class DynamicAnalyzer:
    """محرك التحليل الديناميكي للبرامج الضارة"""
    
    def __init__(self):
        self.results = {}
        self.monitoring = False
        self.process = None
        self.network_connections = []
        self.file_operations = []
        self.registry_operations = []
        self.process_activities = []
        
    def analyze_file(self, file_path, timeout=60):
        """تحليل ملف بشكل ديناميكي"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"الملف غير موجود: {file_path}")
                
            self.results = {
                'file_path': file_path,
                'timestamp': datetime.now().isoformat(),
                'analysis_duration': timeout,
                'initial_system_state': self._capture_system_state(),
                'execution_results': {},
                'network_activity': [],
                'file_activity': [],
                'process_activity': [],
                'registry_activity': [],
                'final_system_state': {}
            }
            
            # بدء المراقبة
            self._start_monitoring()
            
            # تشغيل الملف
            execution_result = self._execute_file(file_path, timeout)
            self.results['execution_results'] = execution_result
            
            # إيقاف المراقبة
            self._stop_monitoring()
            
            # التقاط الحالة النهائية للنظام
            self.results['final_system_state'] = self._capture_system_state()
            
            # تحليل التغييرات
            self.results['changes_detected'] = self._analyze_changes()
            
            return self.results
            
        except Exception as e:
            self._stop_monitoring()
            return {'error': str(e)}
    
    def _capture_system_state(self):
        """التقاط حالة النظام الحالية"""
        try:
            state = {
                'processes': [p.info for p in psutil.process_iter(['pid', 'name', 'cmdline'])],
                'network_connections': [conn._asdict() for conn in psutil.net_connections()],
                'cpu_percent': psutil.cpu_percent(),
                'memory_info': psutil.virtual_memory()._asdict(),
                'disk_usage': psutil.disk_usage('/')._asdict() if os.name != 'nt' else psutil.disk_usage('C:')._asdict()
            }
            return state
        except Exception as e:
            return {'error': str(e)}
    
    def _start_monitoring(self):
        """بدء مراقبة النشاطات"""
        self.monitoring = True
        self.network_connections = []
        self.file_operations = []
        self.process_activities = []
        
        # بدء خيوط المراقبة
        threading.Thread(target=self._monitor_network, daemon=True).start()
        threading.Thread(target=self._monitor_processes, daemon=True).start()
        threading.Thread(target=self._monitor_files, daemon=True).start()
    
    def _stop_monitoring(self):
        """إيقاف المراقبة"""
        self.monitoring = False
        
        # إنهاء العملية إذا كانت لا تزال تعمل
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                try:
                    self.process.kill()
                except:
                    pass
    
    def _execute_file(self, file_path, timeout):
        """تشغيل الملف ومراقبة تنفيذه"""
        try:
            start_time = time.time()
            
            # تشغيل الملف
            self.process = subprocess.Popen(
                [file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )
            
            # انتظار انتهاء التنفيذ أو انتهاء المهلة الزمنية
            try:
                stdout, stderr = self.process.communicate(timeout=timeout)
                return_code = self.process.returncode
            except subprocess.TimeoutExpired:
                self.process.kill()
                stdout, stderr = self.process.communicate()
                return_code = -1
            
            execution_time = time.time() - start_time
            
            return {
                'return_code': return_code,
                'execution_time': execution_time,
                'stdout': stdout.decode('utf-8', errors='ignore') if stdout else '',
                'stderr': stderr.decode('utf-8', errors='ignore') if stderr else '',
                'timeout_occurred': execution_time >= timeout
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _monitor_network(self):
        """مراقبة الاتصالات الشبكية"""
        initial_connections = set()
        try:
            # الحصول على الاتصالات الأولية
            for conn in psutil.net_connections():
                if conn.laddr and conn.raddr:
                    initial_connections.add((conn.laddr.ip, conn.laddr.port, conn.raddr.ip, conn.raddr.port))
        except:
            pass
            
        while self.monitoring:
            try:
                current_connections = psutil.net_connections()
                for conn in current_connections:
                    if conn.laddr and conn.raddr:
                        conn_tuple = (conn.laddr.ip, conn.laddr.port, conn.raddr.ip, conn.raddr.port)
                        if conn_tuple not in initial_connections:
                            self.network_connections.append({
                                'timestamp': datetime.now().isoformat(),
                                'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                                'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}",
                                'status': conn.status,
                                'pid': conn.pid
                            })
                            initial_connections.add(conn_tuple)
                
                time.sleep(1)
            except:
                time.sleep(1)
                continue
    
    def _monitor_processes(self):
        """مراقبة العمليات الجديدة"""
        initial_processes = set()
        try:
            for p in psutil.process_iter(['pid']):
                initial_processes.add(p.info['pid'])
        except:
            pass
            
        while self.monitoring:
            try:
                current_processes = psutil.process_iter(['pid', 'name', 'cmdline', 'create_time'])
                for p in current_processes:
                    if p.info['pid'] not in initial_processes:
                        self.process_activities.append({
                            'timestamp': datetime.now().isoformat(),
                            'pid': p.info['pid'],
                            'name': p.info['name'],
                            'cmdline': ' '.join(p.info['cmdline']) if p.info['cmdline'] else '',
                            'create_time': datetime.fromtimestamp(p.info['create_time']).isoformat()
                        })
                        initial_processes.add(p.info['pid'])
                
                time.sleep(2)
            except:
                time.sleep(2)
                continue
    
    def _monitor_files(self):
        """مراقبة عمليات الملفات (محاكاة)"""
        # هذه دالة محاكاة لمراقبة الملفات
        # في التطبيق الحقيقي، ستحتاج لاستخدام مكتبات متخصصة
        while self.monitoring:
            try:
                # محاكاة اكتشاف تغييرات الملفات
                # يمكن تطوير هذا باستخدام watchdog أو مكتبات أخرى
                time.sleep(5)
            except:
                time.sleep(5)
                continue
    
    def _analyze_changes(self):
        """تحليل التغييرات التي حدثت"""
        changes = {
            'network_activity_detected': len(self.network_connections) > 0,
            'new_processes_created': len(self.process_activities) > 0,
            'suspicious_network_connections': self._find_suspicious_connections(),
            'suspicious_processes': self._find_suspicious_processes()
        }
        
        # إضافة البيانات المجمعة
        self.results['network_activity'] = self.network_connections
        self.results['process_activity'] = self.process_activities
        self.results['file_activity'] = self.file_operations
        
        return changes
    
    def _find_suspicious_connections(self):
        """البحث عن اتصالات مشبوهة"""
        suspicious = []
        
        for conn in self.network_connections:
            remote_ip = conn['remote_address'].split(':')[0]
            
            # فحص عناوين IP المشبوهة
            if self._is_suspicious_ip(remote_ip):
                suspicious.append({
                    'connection': conn,
                    'reason': 'عنوان IP مشبوه'
                })
            
            # فحص المنافذ المشبوهة
            remote_port = int(conn['remote_address'].split(':')[1])
            if remote_port in [4444, 5555, 6666, 8080, 9999]:
                suspicious.append({
                    'connection': conn,
                    'reason': 'منفذ مشبوه'
                })
        
        return suspicious
    
    def _find_suspicious_processes(self):
        """البحث عن عمليات مشبوهة"""
        suspicious = []
        
        for proc in self.process_activities:
            # فحص أسماء العمليات المشبوهة
            suspicious_names = ['cmd.exe', 'powershell.exe', 'nc.exe', 'netcat.exe']
            if any(name in proc['name'].lower() for name in suspicious_names):
                suspicious.append({
                    'process': proc,
                    'reason': 'اسم عملية مشبوه'
                })
            
            # فحص معاملات سطر الأوامر المشبوهة
            cmdline = proc['cmdline'].lower()
            suspicious_args = ['download', 'wget', 'curl', 'invoke-webrequest', 'base64']
            if any(arg in cmdline for arg in suspicious_args):
                suspicious.append({
                    'process': proc,
                    'reason': 'معاملات سطر أوامر مشبوهة'
                })
        
        return suspicious
    
    def _is_suspicious_ip(self, ip):
        """فحص ما إذا كان عنوان IP مشبوهاً"""
        # قائمة بسيطة من عناوين IP المشبوهة (يمكن توسيعها)
        suspicious_ips = [
            '127.0.0.1',  # localhost (قد يكون مشبوهاً في بعض السياقات)
        ]
        
        # فحص النطاقات الخاصة
        private_ranges = [
            '10.',
            '172.16.',
            '192.168.'
        ]
        
        # إذا كان IP خارج النطاقات الخاصة، قد يكون مشبوهاً
        if not any(ip.startswith(range_) for range_ in private_ranges) and ip != '127.0.0.1':
            return True
            
        return ip in suspicious_ips
    
    def generate_report(self, output_format='json'):
        """إنشاء تقرير التحليل"""
        if output_format == 'json':
            return json.dumps(self.results, indent=2, ensure_ascii=False)
        elif output_format == 'text':
            return self._generate_text_report()
        else:
            raise ValueError("تنسيق غير مدعوم")
    
    def _generate_text_report(self):
        """إنشاء تقرير نصي"""
        report = []
        report.append("=" * 60)
        report.append("تقرير التحليل الديناميكي - أداة Mijhar")
        report.append("=" * 60)
        report.append(f"الملف: {self.results.get('file_path', 'غير محدد')}")
        report.append(f"وقت التحليل: {self.results.get('timestamp', 'غير محدد')}")
        report.append(f"مدة التحليل: {self.results.get('analysis_duration', 0)} ثانية")
        report.append("")
        
        # نتائج التنفيذ
        exec_results = self.results.get('execution_results', {})
        report.append("نتائج التنفيذ:")
        report.append(f"  كود الإرجاع: {exec_results.get('return_code', 'غير محدد')}")
        report.append(f"  وقت التنفيذ: {exec_results.get('execution_time', 0):.2f} ثانية")
        report.append(f"  انتهت المهلة الزمنية: {'نعم' if exec_results.get('timeout_occurred', False) else 'لا'}")
        report.append("")
        
        # النشاط الشبكي
        network_activity = self.results.get('network_activity', [])
        report.append(f"النشاط الشبكي: {len(network_activity)} اتصال")
        for conn in network_activity[:5]:  # أول 5 اتصالات
            report.append(f"  - {conn['local_address']} -> {conn['remote_address']}")
        report.append("")
        
        # نشاط العمليات
        process_activity = self.results.get('process_activity', [])
        report.append(f"العمليات الجديدة: {len(process_activity)} عملية")
        for proc in process_activity[:5]:  # أول 5 عمليات
            report.append(f"  - {proc['name']} (PID: {proc['pid']})")
        
        return "\n".join(report)

if __name__ == "__main__":
    # اختبار المحرك
    analyzer = DynamicAnalyzer()
    print("محرك التحليل الديناميكي جاهز للاستخدام")
