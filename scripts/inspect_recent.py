import os, sys
# ensure project root is on sys.path so `pr1` settings can be imported
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pr1.settings')
import django
django.setup()
from editor.models import Asset
recent=Asset.objects.filter(title__startswith='Gen:').order_by('-created_at')[:10]
for a in recent:
    print('ID:', a.id)
    print(' title:', a.title)
    print(' image.name:', getattr(a.image,'name',None))
    try:
        print(' image.url:', a.image.url)
    except Exception as e:
        print(' image.url: ERROR', e)
    fs_path = os.path.join(os.getcwd(), 'media', a.image.name) if getattr(a.image,'name',None) else None
    print(' file exists at', fs_path, os.path.exists(fs_path) if fs_path else None)
    print('---')
