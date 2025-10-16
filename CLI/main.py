
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mijhar - Command Line Interface
واجهة سطر الأوامر لأداة Mijhar

Author: Hassan Mohamed Hassan Ahmed
GitHub: kush-king249
"""

import click
import os
import sys
import json
from datetime import datetime

# إضافة مسار الواجهة الخلفية
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from static_analyzer import StaticAnalyzer
from dynamic_analyzer import DynamicAnalyzer
from reports_generator import ReportsGenerator

@click.group()
@click.version_option(version='1.0.0', prog_name='Mijhar')
def cli():
    """
    🛡️ Mijhar - أداة تحليل البرامج الضارة المتقدمة
    
    أداة شاملة للتحليل الثابت والديناميكي للبرامج الضارة
    تم تطويرها بواسطة Hassan Mohamed Hassan Ahmed
    """
    pass

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='report.json', help='مسار ملف التقرير')
@click.option('--format', '-f', type=click.Choice(['json', 'text']), default='json', help='تنسيق التقرير')
@click.option('--verbose', '-v', is_flag=True, help='عرض تفاصيل إضافية')
def static(file_path, output, format, verbose):
    """تحليل ملف بشكل ثابت"""
    
    if verbose:
        click.echo("🔍 بدء التحليل الثابت...")
        click.echo(f"📁 الملف: {file_path}")
    
    try:
        # إنشاء محلل ثابت
        analyzer = StaticAnalyzer()
        
        # تحليل الملف
        with click.progressbar(length=100, label='جاري التحليل') as bar:
            bar.update(20)
            results = analyzer.analyze_file(file_path)
            bar.update(80)
        
        if 'error' in results:
            click.echo(f"❌ خطأ في التحليل: {results['error']}", err=True)
            sys.exit(1)
        
        # إنشاء التقرير
        report_content = analyzer.generate_report(format)
        
        # حفظ التقرير
        with open(output, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        if verbose:
            click.echo(f"✅ تم إكمال التحليل الثابت")
            click.echo(f"📄 التقرير محفوظ في: {output}")
            
            # عرض ملخص النتائج
            click.echo("\n📊 ملخص النتائج:")
            file_info = results.get('file_info', {})
            click.echo(f"   الحجم: {file_info.get('size', 0):,} بايت")
            
            hashes = results.get('hashes', {})
            if hashes:
                click.echo(f"   MD5: {hashes.get('md5', 'غير متوفر')}")
            
            indicators = results.get('suspicious_indicators', [])
            click.echo(f"   المؤشرات المشبوهة: {len(indicators)}")
        else:
            click.echo(f"تم حفظ التقرير في: {output}")
            
    except Exception as e:
        click.echo(f"❌ خطأ: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='report.json', help='مسار ملف التقرير')
@click.option('--format', '-f', type=click.Choice(['json', 'text']), default='json', help='تنسيق التقرير')
@click.option('--timeout', '-t', default=60, help='المهلة الزمنية بالثواني')
@click.option('--verbose', '-v', is_flag=True, help='عرض تفاصيل إضافية')
def dynamic(file_path, output, format, timeout, verbose):
    """تحليل ملف بشكل ديناميكي"""
    
    if verbose:
        click.echo("⚡ بدء التحليل الديناميكي...")
        click.echo(f"📁 الملف: {file_path}")
        click.echo(f"⏱️ المهلة الزمنية: {timeout} ثانية")
    
    try:
        # إنشاء محلل ديناميكي
        analyzer = DynamicAnalyzer()
        
        # تحليل الملف
        with click.progressbar(length=100, label='جاري التحليل') as bar:
            bar.update(10)
            results = analyzer.analyze_file(file_path, timeout)
            bar.update(90)
        
        if 'error' in results:
            click.echo(f"❌ خطأ في التحليل: {results['error']}", err=True)
            sys.exit(1)
        
        # إنشاء التقرير
        report_content = analyzer.generate_report(format)
        
        # حفظ التقرير
        with open(output, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        if verbose:
            click.echo(f"✅ تم إكمال التحليل الديناميكي")
            click.echo(f"📄 التقرير محفوظ في: {output}")
            
            # عرض ملخص النتائج
            click.echo("\n📊 ملخص النتائج:")
            exec_results = results.get('execution_results', {})
            click.echo(f"   كود الإرجاع: {exec_results.get('return_code', 'غير محدد')}")
            click.echo(f"   وقت التنفيذ: {exec_results.get('execution_time', 0):.2f} ثانية")
            
            network_activity = results.get('network_activity', [])
            click.echo(f"   الاتصالات الشبكية: {len(network_activity)}")
            
            process_activity = results.get('process_activity', [])
            click.echo(f"   العمليات الجديدة: {len(process_activity)}")
        else:
            click.echo(f"تم حفظ التقرير في: {output}")
            
    except Exception as e:
        click.echo(f"❌ خطأ: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='combined_report.html', help='مسار ملف التقرير')
@click.option('--format', '-f', type=click.Choice(['html', 'json', 'text']), default='html', help='تنسيق التقرير')
@click.option('--timeout', '-t', default=60, help='المهلة الزمنية للتحليل الديناميكي')
@click.option('--static-only', is_flag=True, help='التحليل الثابت فقط')
@click.option('--dynamic-only', is_flag=True, help='التحليل الديناميكي فقط')
@click.option('--verbose', '-v', is_flag=True, help='عرض تفاصيل إضافية')
def analyze(file_path, output, format, timeout, static_only, dynamic_only, verbose):
    """تحليل شامل للملف (ثابت + ديناميكي)"""
    
    if static_only and dynamic_only:
        click.echo("❌ لا يمكن استخدام --static-only و --dynamic-only معاً", err=True)
        sys.exit(1)
    
    if verbose:
        click.echo("🛡️ بدء التحليل الشامل...")
        click.echo(f"📁 الملف: {file_path}")
        
        analysis_types = []
        if not dynamic_only:
            analysis_types.append("ثابت")
        if not static_only:
            analysis_types.append("ديناميكي")
        click.echo(f"🔍 أنواع التحليل: {', '.join(analysis_types)}")
    
    try:
        static_results = {}
        dynamic_results = {}
        
        # التحليل الثابت
        if not dynamic_only:
            if verbose:
                click.echo("\n🔍 بدء التحليل الثابت...")
            
            static_analyzer = StaticAnalyzer()
            with click.progressbar(length=50, label='التحليل الثابت') as bar:
                static_results = static_analyzer.analyze_file(file_path)
                bar.update(50)
            
            if 'error' in static_results:
                click.echo(f"⚠️ خطأ في التحليل الثابت: {static_results['error']}")
                static_results = {}
        
        # التحليل الديناميكي
        if not static_only:
            if verbose:
                click.echo("\n⚡ بدء التحليل الديناميكي...")
            
            dynamic_analyzer = DynamicAnalyzer()
            with click.progressbar(length=50, label='التحليل الديناميكي') as bar:
                dynamic_results = dynamic_analyzer.analyze_file(file_path, timeout)
                bar.update(50)
            
            if 'error' in dynamic_results:
                click.echo(f"⚠️ خطأ في التحليل الديناميكي: {dynamic_results['error']}")
                dynamic_results = {}
        
        # إنشاء التقرير المدمج
        if verbose:
            click.echo("\n📄 إنشاء التقرير المدمج...")
        
        reports_generator = ReportsGenerator()
        report_result = reports_generator.generate_combined_report(
            static_results, dynamic_results, format
        )
        
        if 'error' in report_result:
            click.echo(f"❌ خطأ في إنشاء التقرير: {report_result['error']}", err=True)
            sys.exit(1)
        
        # نسخ التقرير إلى المسار المطلوب
        if report_result['report_path'] != output:
            import shutil
            shutil.copy2(report_result['report_path'], output)
        
        if verbose:
            click.echo(f"✅ تم إكمال التحليل الشامل")
            click.echo(f"📄 التقرير محفوظ في: {output}")
            click.echo(f"🆔 معرف التقرير: {report_result['report_id']}")
            
            # عرض ملخص النتائج
            click.echo("\n📊 ملخص النتائج:")
            
            if static_results and 'suspicious_indicators' in static_results:
                indicators = static_results['suspicious_indicators']
                click.echo(f"   المؤشرات المشبوهة (ثابت): {len(indicators)}")
            
            if dynamic_results and 'network_activity' in dynamic_results:
                network_activity = dynamic_results['network_activity']
                click.echo(f"   الاتصالات الشبكية: {len(network_activity)}")
            
            if dynamic_results and 'process_activity' in dynamic_results:
                process_activity = dynamic_results['process_activity']
                click.echo(f"   العمليات الجديدة: {len(process_activity)}")
        else:
            click.echo(f"تم حفظ التقرير في: {output}")
            
    except Exception as e:
        click.echo(f"❌ خطأ: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('report_path', type=click.Path(exists=True))
def view(report_path):
    """عرض تقرير محفوظ"""
    
    try:
        if report_path.endswith('.json'):
            with open(report_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            click.echo("📄 عرض التقرير:")
            click.echo("=" * 50)
            
            if 'report_id' in data:
                click.echo(f"🆔 معرف التقرير: {data['report_id']}")
            
            if 'timestamp' in data:
                click.echo(f"⏰ وقت الإنشاء: {data['timestamp']}")
            
            if 'summary' in data:
                summary = data['summary']
                click.echo(f"📁 الملف: {summary.get('file_analyzed', 'غير محدد')}")
                
                findings = summary.get('key_findings', [])
                if findings:
                    click.echo("\n🔍 النتائج الرئيسية:")
                    for finding in findings:
                        click.echo(f"   • {finding}")
            
            if 'risk_assessment' in data:
                risk = data['risk_assessment']
                click.echo(f"\n⚠️ تقييم المخاطر: {risk.get('level', 'غير محدد')} ({risk.get('score', 0)} نقطة)")
                
                factors = risk.get('factors', [])
                if factors:
                    click.echo("   العوامل:")
                    for factor in factors:
                        click.echo(f"     - {factor}")
        
        elif report_path.endswith('.txt'):
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            click.echo(content)
        
        elif report_path.endswith('.html'):
            click.echo(f"📄 تقرير HTML: {report_path}")
            click.echo("💡 افتح الملف في متصفح الويب لعرضه بشكل كامل")
        
        else:
            click.echo("❌ تنسيق ملف غير مدعوم", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ خطأ في قراءة التقرير: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def info():
    """عرض معلومات حول الأداة"""
    
    click.echo("🛡️ Mijhar - أداة تحليل البرامج الضارة")
    click.echo("=" * 50)
    click.echo("📝 الوصف: أداة شاملة للتحليل الثابت والديناميكي للبرامج الضارة")
    click.echo("👨‍💻 المؤلف: Hassan Mohamed Hassan Ahmed")
    click.echo("🔗 GitHub: kush-king249")
    click.echo("📅 الإصدار: 1.0.0")
    click.echo("")
    click.echo("🔧 الميزات:")
    click.echo("   • التحليل الثابت للملفات التنفيذية")
    click.echo("   • التحليل الديناميكي مع مراقبة السلوك")
    click.echo("   • إنشاء تقارير شاملة بتنسيقات متعددة")
    click.echo("   • واجهة سطر أوامر سهلة الاستخدام")
    click.echo("   • واجهة ويب تفاعلية")
    click.echo("")
    click.echo("📚 للمساعدة: mijhar --help")
    click.echo("🌐 الواجهة الرسومية: python backend/app.py")

if __name__ == '__main__':
    cli()
