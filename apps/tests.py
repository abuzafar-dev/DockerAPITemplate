import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from django.test import SimpleTestCase, TestCase

ROOT = Path(__file__).resolve().parent.parent


def run_with_settings(code, **env):
    full = {k: v for k, v in os.environ.items() if k not in ('DEBUG', 'ALLOWED_HOSTS')}
    full.update({'SECRET_KEY': 'x' * 50, 'DJANGO_SETTINGS_MODULE': 'dockerapitemplate.settings'}, **env)
    return subprocess.run([sys.executable, '-c', code], cwd=ROOT, env=full, capture_output=True, text=True)


class ProductionConfigTests(SimpleTestCase):
    def test_static_files_served_when_debug_false(self):
        code = (
            "import os, django; from django.conf import settings; "
            "settings.STATIC_ROOT = os.environ['TMP_STATIC']; django.setup(); "
            "from django.core.management import call_command; "
            "call_command('collectstatic', '--noinput', verbosity=0); "
            "from django.test import Client; "
            "print(Client().get('/static/admin/css/base.css').status_code)"
        )
        result = run_with_settings(code, DEBUG='False', ALLOWED_HOSTS='testserver',
                                   TMP_STATIC=tempfile.mkdtemp())
        self.assertEqual(result.stdout.strip(), '200', result.stderr)

    def test_safe_defaults_when_env_missing(self):
        # Lokal .env bo'lmagan nusxada: faqat koddagi standart qiymatlar tekshiriladi
        import shutil
        copy = Path(tempfile.mkdtemp()) / 'project'
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.env', '.git', '*.sqlite3', 'staticfiles'))
        code = "from django.conf import settings as s; print(s.DEBUG, s.ALLOWED_HOSTS)"
        env = {k: v for k, v in os.environ.items() if k not in ('DEBUG', 'ALLOWED_HOSTS', 'DATABASE_URL')}
        env.update(SECRET_KEY='x' * 50, DJANGO_SETTINGS_MODULE='dockerapitemplate.settings')
        result = subprocess.run([sys.executable, '-c', code], cwd=copy, env=env, capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), "False ['localhost', '127.0.0.1']", result.stderr)

    def test_postgres_not_published_publicly(self):
        compose = yaml.safe_load((ROOT / 'docker-compose.yml').read_text())
        for port in compose['services']['db'].get('ports', []):
            self.assertTrue(str(port).startswith('127.0.0.1:'), port)


class HealthCheckTests(TestCase):
    def test_health(self):
        self.assertEqual(self.client.get('/api/health/').json(), {'status': 'ok'})
