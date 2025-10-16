
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mijhar - Main Runner
ملف التشغيل الرئيسي لأداة Mijhar

Author: Hassan Mohamed Hassan Ahmed
GitHub: kush-king249
"""

import sys
import os
import argparse
from pathlib import Path

# إضافة مسارات المشروع
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'backend'))
sys.path.insert(0, str(project_root / 'cli'))

def print_banner():
    """طباعة شعار الأداة"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🛡️  Mijhar - أداة تحليل البرامج الضارة المتقدمة  🛡️     ║
    ║                                                              ║
    ║    المؤلف: Hassan Mohamed Hassan Ahmed                       ║
    ║    GitHub: kush-king249                                      ║
    ║    الإصدار: 1.0.0                                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_web_interface():
    """تشغيل الواجهة الرسومية (Web)"""
    try:
        from backend.app import app
        print("🌐 بدء تشغيل الواجهة الرسومية...")
        print("📍 الواجهة متاحة على: http://localhost:5000")
        print("🔗 API متاح على: http://localhost:5000/api/")
        print("⏹️  اضغط Ctrl+C للإيقاف")
        print("-" * 60)
        app.run(debug=False, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ خطأ في استيراد الواجهة الرسومية: {e}")
        print("💡 تأكد من تثبيت المكتبات المطلوبة: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ في تشغيل الواجهة الرسومية: {e}")
        sys.exit(1)

def run_cli():
    """تشغيل واجهة سطر الأوامر"""
    try:
        from cli.main import cli
        # إزالة المعامل الأول (اسم الملف) وتمرير باقي المعاملات
        sys.argv = ['mijhar'] + sys.argv[2:]
        cli()
    except ImportError as e:
        print(f"❌ خطأ في استيراد واجهة سطر الأوامر: {e}")
        print("💡 تأكد من تثبيت المكتبات المطلوبة: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ في تشغيل واجهة سطر الأوامر: {e}")
        sys.exit(1)


def main():
    """الدالة الرئيسية"""
    print_banner()
    
    # إعداد معالج الحجج
    parser = argparse.ArgumentParser(
        description='Mijhar - أداة تحليل البرامج الضارة المتقدمة',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
  python run.py web                    # تشغيل الواجهة الرسومية
  python run.py cli --help             # عرض مساعدة سطر الأوامر
  python run.py cli analyze file.exe   # تحليل ملف
  python run.py cli static file.exe    # تحليل ثابت فقط
  python run.py cli dynamic file.exe   # تحليل ديناميكي فقط
        """
    )
    
    parser.add_argument(
        'mode',
        choices=['web', 'cli'],
        help='وضع التشغيل: web للواجهة الرسومية، cli لسطر الأوامر'
    )
    
    # تحليل الحجج
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    

    
    mode = sys.argv[1]
    
    if mode == 'web':
        run_web_interface()
    elif mode == 'cli':
        run_cli()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 تم إيقاف البرنامج بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        sys.exit(1)
