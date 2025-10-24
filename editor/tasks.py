import os
import uuid
import requests
from django.conf import settings
from celery import shared_task
from .models import GeneratorJob, Asset


@shared_task(bind=True)
def hf_generate_task(self, job_id, model_name=None):
    """Call Hugging Face Inference API to generate images for a GeneratorJob.

    Requires HUGGINGFACE_API_TOKEN in settings or environment.
    """
    job = GeneratorJob.objects.get(pk=job_id)
    prompt = job.prompt
    count = job.count
    size = job.size
    model = model_name or settings.HUGGINGFACE_DEFAULT_MODEL

    token = settings.HUGGINGFACE_API_TOKEN
    if not token:
        raise RuntimeError('Hugging Face API token not configured')

    headers = {
        'Authorization': f'Bearer {token}'
    }

    width, height = map(int, size.split('x')) if 'x' in size else (512, 512)

    generated = []
    for i in range(count):
        # HF Inference API expects JSON with inputs and optional parameters
        payload = {
            'inputs': prompt,
            'parameters': {
                'width': width,
                'height': height,
            }
        }
        url = f'https://api-inference.huggingface.co/models/{model}'
        resp = requests.post(url, headers=headers, json=payload, stream=True, timeout=300)
        if resp.status_code != 200:
            raise RuntimeError(f'HF API error: {resp.status_code} {resp.text[:200]}')

        content_type = resp.headers.get('content-type','')
        # If the model returns an image binary
        if content_type.startswith('image/'):
            ext = 'png' if 'png' in content_type else 'jpg'
            filename = f"hf_{uuid.uuid4().hex[:8]}.{ext}"
            out_dir = os.path.join(settings.MEDIA_ROOT, 'generated')
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, filename)
            with open(out_path, 'wb') as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)

            asset = Asset.objects.create(title=f"Gen: {prompt[:40]}", image='generated/' + filename)
            job.result_assets.add(asset)
            generated.append(asset.id)
        else:
            # Some HF models return base64 JSON or JSON with images; attempt to parse
            data = resp.content
            # try to save raw content as PNG
            filename = f"hf_{uuid.uuid4().hex[:8]}.bin"
            out_dir = os.path.join(settings.MEDIA_ROOT, 'generated')
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, filename)
            with open(out_path, 'wb') as f:
                f.write(data)
            asset = Asset.objects.create(title=f"Gen: {prompt[:40]}", image='generated/' + filename)
            job.result_assets.add(asset)
            generated.append(asset.id)

    job.completed = True
    job.save()
    return {'generated': generated}
