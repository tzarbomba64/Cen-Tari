const tabs = document.querySelectorAll('.tab-button');
tabs.forEach(btn => btn.onclick = () => {
  tabs.forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(btn.dataset.tab).classList.add('active');
});

// Helper to call backend
async function callAPI(action, payload={}) {
  const resp = await fetch(`/main.py/${action}`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  });
  return resp.json();
}

document.getElementById('run').onclick = async ()=>{
  const code = document.getElementById('editor').value;
  const res  = await callAPI('run', {code});
  document.getElementById('output').innerHTML = res.html;
  document.getElementById('terminal').textContent += res.log;
};

['patch','build','log','execute','variable','package'].forEach(id=>{
  document.getElementById(id).onclick = async ()=>{
    const code = document.getElementById('editor').value;
    const res  = await callAPI(id, {code});
    if(res.html) document.getElementById('output').innerHTML = res.html;
    if(res.log) document.getElementById('terminal').textContent += res.log;
  };
});
