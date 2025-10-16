
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mijhar - Static Analysis Engine
محرك التحليل الثابت لأداة Mijhar

Author: Hassan Mohamed Hassan Ahmed
GitHub: kush-king249
"""

import pefile
import hashlib
import os
import json
from datetime import datetime
import re
import struct

class StaticAnalyzer:
    """محرك التحليل الثابت للبرامج الضارة"""
    
    def __init__(self):
        self.results = {}
        
    def analyze_file(self, file_path):
        """تحليل ملف بشكل ثابت"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"الملف غير موجود: {file_path}")
                
            self.results = {
                'file_path': file_path,
                'timestamp': datetime.now().isoformat(),
                'file_info': self._get_file_info(file_path),
                'hashes': self._calculate_hashes(file_path),
                'pe_analysis': self._analyze_pe(file_path),
                'strings': self._extract_strings(file_path),
                'entropy': self._calculate_entropy(file_path),
                'suspicious_indicators': self._find_suspicious_indicators(file_path)
            }
            
            return self.results
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_file_info(self, file_path):
        """الحصول على معلومات الملف الأساسية"""
        stat = os.stat(file_path)
        return {
            'size': stat.st_size,
            'creation_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modification_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'extension': os.path.splitext(file_path)[1].lower()
        }
    
    def _calculate_hashes(self, file_path):
        """حساب الهاشات المختلفة للملف"""
        hashes = {}
        
        with open(file_path, 'rb') as f:
            data = f.read()
            
        hashes['md5'] = hashlib.md5(data).hexdigest()
        hashes['sha1'] = hashlib.sha1(data).hexdigest()
        hashes['sha256'] = hashlib.sha256(data).hexdigest()
        
        return hashes
    
    def _analyze_pe(self, file_path):
        """تحليل ملف PE"""
        try:
            pe = pefile.PE(file_path)
            
            # معلومات الأقسام
            sections = []
            for section in pe.sections:
                sections.append({
                    'name': section.Name.decode().strip('\x00'),
                    'virtual_address': hex(section.VirtualAddress),
                    'virtual_size': section.Misc_VirtualSize,
                    'raw_size': section.SizeOfRawData,
                    'entropy': section.get_entropy()
                })
            
            # الوظائف المستوردة
            imports = []
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    dll_name = entry.dll.decode()
                    functions = []
                    for imp in entry.imports:
                        if imp.name:
                            functions.append(imp.name.decode())
                    imports.append({
                        'dll': dll_name,
                        'functions': functions
                    })
            
            # الوظائف المصدرة
            exports = []
            if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
                for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                    if exp.name:
                        exports.append(exp.name.decode())
            
            return {
                'machine_type': hex(pe.FILE_HEADER.Machine),
                'timestamp': datetime.fromtimestamp(pe.FILE_HEADER.TimeDateStamp).isoformat(),
                'entry_point': hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
                'sections': sections,
                'imports': imports,
                'exports': exports,
                'is_dll': pe.is_dll(),
                'is_exe': pe.is_exe()
            }
            
        except Exception as e:
            return {'error': f'خطأ في تحليل PE: {str(e)}'}
    
    def _extract_strings(self, file_path, min_length=4):
        """استخراج النصوص من الملف"""
        strings = []
        
        with open(file_path, 'rb') as f:
            data = f.read()
            
        # البحث عن النصوص ASCII
        ascii_strings = re.findall(b'[\\x20-\\x7E]{' + str(min_length).encode() + b',}', data)
        for s in ascii_strings:
            strings.append(s.decode('ascii', errors='ignore'))
            
        # البحث عن النصوص Unicode
        unicode_strings = re.findall(b'(?:[\\x20-\\x7E]\\x00){' + str(min_length).encode() + b',}', data)
        for s in unicode_strings:
            strings.append(s.decode('utf-16le', errors='ignore'))
            
        return list(set(strings))[:100]  # أول 100 نص فريد
    
    def _calculate_entropy(self, file_path):
        """حساب الإنتروبيا للملف"""
        with open(file_path, 'rb') as f:
            data = f.read()
            
        if not data:
            return 0
            
        # حساب تكرار كل بايت
        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1
            
        # حساب الإنتروبيا
        entropy = 0
        data_len = len(data)
        
        for count in byte_counts:
            if count > 0:
                probability = count / data_len
                entropy -= probability * (probability.bit_length() - 1)
                
        return entropy
    
    def _find_suspicious_indicators(self, file_path):
        """البحث عن مؤشرات مشبوهة"""
        indicators = []
        
        # قراءة الملف
        with open(file_path, 'rb') as f:
            data = f.read()
            
        # البحث عن عناوين IP
        ip_pattern = rb'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ips = re.findall(ip_pattern, data)
        if ips:
            indicators.append({
                'type': 'IP_ADDRESSES',
                'description': 'عناوين IP موجودة في الملف',
                'count': len(ips),
                'samples': [ip.decode() for ip in ips[:5]]
            })
            
        # البحث عن URLs
        url_pattern = rb'https?://[^\s<>"{}|\\^`\[\]]*'
        urls = re.findall(url_pattern, data)
        if urls:
            indicators.append({
                'type': 'URLS',
                'description': 'روابط موجودة في الملف',
                'count': len(urls),
                'samples': [url.decode() for url in urls[:5]]
            })
            
        # البحث عن مفاتيح التسجيل
        registry_pattern = rb'HKEY_[A-Z_]+\\[^\\x00]*'
        registry_keys = re.findall(registry_pattern, data)
        if registry_keys:
            indicators.append({
                'type': 'REGISTRY_KEYS',
                'description': 'مفاتيح تسجيل النظام',
                'count': len(registry_keys),
                'samples': [key.decode(errors='ignore') for key in registry_keys[:5]]
            })
            
        # البحث عن أسماء ملفات مشبوهة
        suspicious_files = [b'cmd.exe', b'powershell.exe', b'regedit.exe', b'taskmgr.exe']
        for suspicious_file in suspicious_files:
            if suspicious_file in data:
                indicators.append({
                    'type': 'SUSPICIOUS_FILES',
                    'description': f'مرجع لملف مشبوه: {suspicious_file.decode()}',
                    'file': suspicious_file.decode()
                })
                
        return indicators
    
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
        report.append("تقرير التحليل الثابت - أداة Mijhar")
        report.append("=" * 60)
        report.append(f"الملف: {self.results.get('file_path', 'غير محدد')}")
        report.append(f"وقت التحليل: {self.results.get('timestamp', 'غير محدد')}")
        report.append("")
        
        # معلومات الملف
        file_info = self.results.get('file_info', {})
        report.append("معلومات الملف:")
        report.append(f"  الحجم: {file_info.get('size', 0)} بايت")
        report.append(f"  الامتداد: {file_info.get('extension', 'غير محدد')}")
        report.append("")
        
        # الهاشات
        hashes = self.results.get('hashes', {})
        report.append("الهاشات:")
        for hash_type, hash_value in hashes.items():
            report.append(f"  {hash_type.upper()}: {hash_value}")
        report.append("")
        
        # المؤشرات المشبوهة
        indicators = self.results.get('suspicious_indicators', [])
        if indicators:
            report.append("المؤشرات المشبوهة:")
            for indicator in indicators:
                report.append(f"  - {indicator.get('description', 'غير محدد')}")
        
        return "\n".join(report)

if __name__ == "__main__":
    # اختبار المحرك
    analyzer = StaticAnalyzer()
    print("محرك التحليل الثابت جاهز للاستخدام")
