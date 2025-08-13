const chatEl = document.getElementById('chat');
const chatForm = document.getElementById('chat-form');
const inputEl = document.getElementById('message');
const uploadForm = document.getElementById('upload-form');
const fileEl = document.getElementById('file');
const docsEl = document.getElementById('docs');

let messages = [];

function addMessage(role, content) {
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.innerHTML = `<span class="role">${role}:</span> <span class="content"></span>`;
  div.querySelector('.content').textContent = content;
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

async function refreshDocs() {
  const res = await fetch('/api/docs');
  const data = await res.json();
  docsEl.innerHTML = '';
  (data.documents || []).forEach(d => {
    const p = document.createElement('p');
    p.textContent = `${d.filename} — ${d.chunks} chunks`;
    docsEl.appendChild(p);
  });
}

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = inputEl.value.trim();
  if (!text) return;
  inputEl.value = '';
  messages.push({ role: 'user', content: text });
  addMessage('user', text);
  addMessage('assistant', '…');

  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages })
  });
  const data = await res.json();
  messages.push({ role: 'assistant', content: data.reply });
  chatEl.lastChild.querySelector('.content').textContent = data.reply;
});

uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!fileEl.files[0]) return;
  const fd = new FormData();
  fd.append('file', fileEl.files[0]);
  const res = await fetch('/api/upload', { method: 'POST', body: fd });
  if (res.ok) {
    await refreshDocs();
  }
});

refreshDocs();



