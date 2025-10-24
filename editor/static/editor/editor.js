// Minimal editor client: preview using Konva and simple action stack + autosave
(function(){
  const assetId = window.EDITOR_ASSET_ID;
  let actions = window.EDITOR_EDITS || [];
  let undoStack = [];

  const stageWidth = 800;
  const stageHeight = 600;

  const stage = new Konva.Stage({
    container: 'stage-container',
    width: stageWidth,
    height: stageHeight,
  });
  const layer = new Konva.Layer();
  stage.add(layer);

  const img = new Image();
  img.onload = function(){
    const kImg = new Konva.Image({
      image: img,
      x: 0, y: 0,
      draggable: false,
    });
    layer.add(kImg);
    // scale image to fit stage while preserving aspect ratio
    const imgW = img.width;
    const imgH = img.height;
    const ratio = Math.min(stageWidth / imgW, stageHeight / imgH, 1);
    kImg.width(imgW * ratio);
    kImg.height(imgH * ratio);
    kImg.x((stageWidth - kImg.width()) / 2);
    kImg.y((stageHeight - kImg.height()) / 2);
    layer.draw();
    window._konvaImage = kImg;
    applyAllActions();
  };
  img.crossOrigin = 'anonymous';
  // choose processed preview if available, otherwise original
  img.src = (window.EDITOR_PROCESSED_URL && window.EDITOR_PROCESSED_URL.length) ? window.EDITOR_PROCESSED_URL : window.EDITOR_IMAGE_URL;
  if(img.src && img.src.indexOf('http') !== 0){
    img.src = window.location.origin + img.src;
  }

  // fallback: load image URL from DOM by requesting asset info via data attributes
  // Instead, derive original from /media path attached in template via asset.image.url
  (function loadOriginal(){
    // find original URL in a hidden image if present
    // We will try to fetch /media/processed or original via api
    // For now request asset info endpoint would be better; fallback: try known path
  })();

  function pushAction(a){
    actions.push(a);
    undoStack = []; // clear redo
    applyAllActions();
  }

  function applyAllActions(){
    // For client preview we just modify CSS-like filters on the Konva image
    const k = window._konvaImage;
    if(!k) return;
    // compute combined filter params
    let exposure = 1, contrast = 1, saturation = 1, rotate = 0;
    actions.forEach(a=>{
      if(a.op === 'exposure') exposure = a.value;
      if(a.op === 'contrast') contrast = a.value;
      if(a.op === 'saturation') saturation = a.value;
      if(a.op === 'rotate') rotate = a.deg;
    });
    // Konva filters require enabling them; we'll fake adjustments by using globalComposite operations
    k.rotation(rotate);
    // quick color adjustments using canvas filter is not available; skip and rely on server for export
    layer.batchDraw();
  }

  // wire controls
  document.getElementById('exposure').addEventListener('input', function(){
    pushAction({op:'exposure', value: parseFloat(this.value)});
  });
  document.getElementById('contrast').addEventListener('input', function(){
    pushAction({op:'contrast', value: parseFloat(this.value)});
  });
  document.getElementById('saturation').addEventListener('input', function(){
    pushAction({op:'saturation', value: parseFloat(this.value)});
  });
  document.getElementById('rotate').addEventListener('input', function(){
    pushAction({op:'rotate', deg: parseFloat(this.value)});
  });

  document.getElementById('undo').addEventListener('click', function(){
    if(actions.length===0) return;
    const a = actions.pop();
    undoStack.push(a);
    applyAllActions();
  });
  document.getElementById('redo').addEventListener('click', function(){
    if(undoStack.length===0) return;
    const a = undoStack.pop();
    actions.push(a);
    applyAllActions();
  });

  // CSRF helper
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  document.getElementById('save-actions').addEventListener('click', function(){
    fetch(`/editor/api/save_actions/${assetId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({actions: actions})
    }).then(r=>r.json()).then(console.log).catch(console.error);
  });

  document.getElementById('export').addEventListener('click', function(){
    fetch(`/editor/api/export/${assetId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({actions: actions})
    }).then(r=>r.json()).then(resp=>{
      if(resp.status === 'ok'){
        window.location.href = resp.processed;
      } else {
        alert('Export error: '+(resp.message||'unknown'))
      }
    }).catch(e=>{console.error(e); alert('Export failed')});
  });

  // autosave every 10s when changes
  let lastSaved = JSON.stringify(actions);
  setInterval(()=>{
    if(JSON.stringify(actions) !== lastSaved){
      fetch(`/editor/api/save_actions/${assetId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({actions: actions})
      }).then(r=>r.json()).then(()=>{ lastSaved = JSON.stringify(actions); }).catch(()=>{});
    }
  }, 10000);

})();
// Small JS for preview and slider value display
document.addEventListener('DOMContentLoaded', function () {
  const imageInput = document.querySelector('input[type="file"][name="image"]');
  const previewImage = document.getElementById('preview-image');
  const noPreview = document.getElementById('no-preview');

  if (imageInput) {
    imageInput.addEventListener('change', function (e) {
      const file = e.target.files && e.target.files[0];
      if (!file) {
        previewImage.style.display = 'none';
        noPreview.style.display = 'block';
        return;
      }
      const reader = new FileReader();
      reader.onload = function (ev) {
        previewImage.src = ev.target.result;
        previewImage.style.display = 'block';
        noPreview.style.display = 'none';
      };
      reader.readAsDataURL(file);
    });
  }

  // update slider labels
  function wireSlider(name, labelId) {
    const el = document.querySelector('input[name="' + name + '"]');
    const label = document.getElementById(labelId);
    if (!el || !label) return;
    label.textContent = el.value;
    el.addEventListener('input', function () { label.textContent = el.value; });
  }

  wireSlider('brightness', 'brightness-val');
  wireSlider('contrast', 'contrast-val');
  wireSlider('saturation', 'saturation-val');
});
