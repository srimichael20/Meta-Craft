
/**
 * MetaCraft AI — Indian Script Generator
 * Frontend Application Logic
 */

const API_BASE = '/api';

// State
let selectedLanguage = 'hindi';
let selectedFormat = 'tv_ad_30';

const LANGUAGES = [
  { key: 'english', native: 'English', name: 'English', code: 'EN' },
  { key: 'hindi', native: 'हिन्दी', name: 'Hindi', code: 'HI' },
  { key: 'tamil', native: 'தமிழ்', name: 'Tamil', code: 'TA' },
  { key: 'telugu', native: 'తెలుగు', name: 'Telugu', code: 'TE' },
  { key: 'bengali', native: 'বাংলা', name: 'Bengali', code: 'BN' },
  { key: 'marathi', native: 'मराठी', name: 'Marathi', code: 'MR' },
  { key: 'gujarati', native: 'ગુજરાતી', name: 'Gujarati', code: 'GU' },
  { key: 'kannada', native: 'ಕನ್ನಡ', name: 'Kannada', code: 'KN' },
  { key: 'malayalam', native: 'മലയാളം', name: 'Malayalam', code: 'ML' },
  { key: 'punjabi', native: 'ਪੰਜਾਬੀ', name: 'Punjabi', code: 'PA' },
];

const FORMATS = [
  { key: 'tv_ad_30', name: 'TV Ad 30s', icon: 'monitor' },
  { key: 'tv_ad_60', name: 'TV Ad 60s', icon: 'film' },
  { key: 'radio_spot', name: 'Radio Spot', icon: 'mic' },
  { key: 'social_reel', name: 'Social Reel', icon: 'smartphone' },
  { key: 'ott_preroll', name: 'OTT Pre-roll', icon: 'play-circle' },
];

// ── Init ───────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  renderLanguageGrid();
  renderFormatGrid();
  renderShowcaseGrid();
  checkHealth();
});

// ── Render UI Components ──────────────────────
function renderLanguageGrid() {
  const grid = document.getElementById('languageGrid');
  grid.innerHTML = LANGUAGES.map(lang => `
    <button class="lang-btn ${lang.key === selectedLanguage ? 'active' : ''}"
            id="lang-${lang.key}"
            onclick="selectLanguage('${lang.key}')">
      <span class="lang-native">${lang.native}</span>
      <span class="lang-name">${lang.name}</span>
    </button>
  `).join('');
}

function renderFormatGrid() {
  const grid = document.getElementById('formatGrid');
  grid.innerHTML = FORMATS.map(fmt => `
    <button class="format-btn ${fmt.key === selectedFormat ? 'active' : ''}"
            id="fmt-${fmt.key}"
            onclick="selectFormat('${fmt.key}')">
      <i data-lucide="${fmt.icon}" class="icon-sm"></i>
      ${fmt.name}
    </button>
  `).join('');
  if (window.lucide) window.lucide.createIcons();
}

function renderShowcaseGrid() {
  const grid = document.getElementById('showcaseGrid');
  grid.innerHTML = LANGUAGES.map(lang => `
    <div class="showcase-item" onclick="selectLanguage('${lang.key}')">
      <div class="showcase-code">${lang.code}</div>
      <div class="showcase-native">${lang.native}</div>
      <div class="showcase-name">${lang.name}</div>
    </div>
  `).join('');
}

// ── Selections ────────────────────────────────
function selectLanguage(key) {
  selectedLanguage = key;
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById(`lang-${key}`);
  if (btn) btn.classList.add('active');
}

function selectFormat(key) {
  selectedFormat = key;
  document.querySelectorAll('.format-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById(`fmt-${key}`);
  if (btn) btn.classList.add('active');
}

// ── Health Check ──────────────────────────────
async function checkHealth() {
  const dot = document.getElementById('statusDot');
  const text = document.getElementById('statusText');
  try {
    const res = await fetch(`${API_BASE}/health`);
    const data = await res.json();
    if (data.ollama_connected && data.model_ready) {
      dot.className = 'status-dot online';
      text.textContent = `${data.model_name} Ready`;
    } else if (data.ollama_connected) {
      dot.className = 'status-dot warning';
      text.textContent = `Model Loading`;
    } else {
      dot.className = 'status-dot offline';
      text.textContent = 'Ollama Offline';
    }
  } catch {
    dot.className = 'status-dot offline';
    text.textContent = 'Server Offline';
  }
}

// ── Generate Script ───────────────────────────
async function generateScript() {
  const brandName = document.getElementById('brandName').value.trim();
  const theme = document.getElementById('theme').value.trim();
  const industry = document.getElementById('industry').value;
  const tone = document.getElementById('tone').value;
  const festival = document.getElementById('festival').value;
  const usp = document.getElementById('usp').value.trim();
  const targetAudience = document.getElementById('targetAudience').value.trim();
  const productDescription = document.getElementById('productDescription').value.trim();

  if (!brandName) { showToast('⚠️ Please enter a brand name', 'error'); return; }
  if (!theme) { showToast('⚠️ Please enter a theme or message', 'error'); return; }

  const lang = LANGUAGES.find(l => l.key === selectedLanguage);
  showLoading(lang?.name || selectedLanguage);
  disableForm(true);

  try {
    const payload = {
      language: selectedLanguage,
      ad_format: selectedFormat,
      brand_name: brandName,
      theme,
      tone,
      industry,
      festival,
      usp,
      target_audience: targetAudience || 'professional Indian audience',
      product_description: productDescription,
    };

    const res = await fetch(`${API_BASE}/scripts/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Generation failed');
    }

    const data = await res.json();
    showResult(data);
    checkHealth();

  } catch (err) {
    showError(err.message || 'Unknown error occurred');
  } finally {
    disableForm(false);
  }
}

// ── UI State Helpers ──────────────────────────
function showLoading(langName) {
  hide('outputEmpty');
  hide('outputResult');
  hide('outputError');
  show('outputLoading');

  document.getElementById('loadingLang').textContent = langName;

  // Animate steps
  const steps = ['step1', 'step2', 'step3', 'step4'];
  let current = 0;
  steps.forEach(s => {
    document.getElementById(s).className = 'step';
  });
  document.getElementById(steps[0]).className = 'step active';

  window._stepInterval = setInterval(() => {
    if (current < steps.length - 1) {
      document.getElementById(steps[current]).className = 'step done';
      current++;
      document.getElementById(steps[current]).className = 'step active';
    }
  }, 2000);
}

function showResult(data) {
  clearInterval(window._stepInterval);
  hide('outputLoading');
  hide('outputEmpty');
  hide('outputError');
  show('outputResult');

  document.getElementById('resultLang').textContent = data.language_native;
  document.getElementById('resultFormat').textContent = data.ad_format;
  document.getElementById('resultDuration').textContent = data.estimated_duration;
  document.getElementById('resultTitle').textContent = data.title;
  document.getElementById('modelBadge').textContent = data.model_used;
  document.getElementById('genTime').textContent = `Generated in ${data.generation_time_sec}s`;

  // Render script with colorized tags
  const formatted = colorizeScript(data.script);
  document.getElementById('scriptOutput').innerHTML = formatted;

  // Store raw for copy
  window._rawScript = data.script;
}

function colorizeScript(script) {
  // Escape HTML first
  let safe = script.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  // New Format: Timestamps [0:00 - 0:05]
  safe = safe.replace(/(\[\d+:\d+\s*-\s*\d+:\d+\])/g, '<span style="color:#fbbf24;font-weight:700;display:block;margin-top:16px;margin-bottom:8px;">$1</span>');

  // New Format: Section Headers
  safe = safe.replace(/(Visual:)/g, '<span style="color:#67e8f9;font-weight:600">Visual:</span>');
  safe = safe.replace(/(Audio \(BGM\):|Audio:)/g, '<span style="color:#f472b6;font-weight:600">$1</span>');
  safe = safe.replace(/(Dialogue:)/g, '<span style="color:#fff;font-weight:600">Dialogue:</span>');
  safe = safe.replace(/(Campaign:)/g, '<span style="color:#fbbf24;font-weight:700;font-size:1.1em">Campaign:</span>');

  // Legacy/Dataset Tags (keeping for backward compatibility)
  safe = safe.replace(/(\[SCENE[^\]]*\]:)/g, '<span class="scene-tag">$1</span>');
  safe = safe.replace(/(\[VO[^\]]*\]:|\[ANNOUNCER[^\]]*\]:)/g, '<span class="vo-tag">$1</span>');
  safe = safe.replace(/(\[TAGLINE[^\]]*\]:)/gi, '<span class="tagline-tag">$1</span>');
  safe = safe.replace(/(\[MUSIC[^\]]*\]:)/g, '<span style="color:#f472b6;font-weight:600">$1</span>');
  safe = safe.replace(/(\[SFX[^\]]*\]:)/g, '<span style="color:#a78bfa;font-weight:600">$1</span>');
  safe = safe.replace(/(\[CUT TO[^\]]*\]:)/g, '<span style="color:#38bdf8;font-weight:600">$1</span>');
  safe = safe.replace(/(\[SUPER\]:)/g, '<span style="color:#fbbf24;font-weight:700">$1</span>');

  // Camera cues inline
  safe = safe.replace(/(CLOSE-UP|WIDE SHOT|SLOW-MO|QUICK CUT|DRONE SHOT|POV SHOT|SPLIT SCREEN|EXTREME CLOSE-UP)/g, '<span style="color:#94a3b8;font-style:italic">$1</span>');

  return safe;
}

function showError(msg) {
  clearInterval(window._stepInterval);
  hide('outputLoading');
  hide('outputEmpty');
  hide('outputResult');
  show('outputError');
  document.getElementById('errorMsg').textContent = msg;
}

function disableForm(disabled) {
  const btn = document.getElementById('generateBtn');
  btn.disabled = disabled;
  btn.querySelector('.btn-text').textContent = disabled ? 'Generating...' : 'Generate Script';
  btn.querySelector('.btn-icon').textContent = disabled ? '⏳' : '✨';
}

function show(id) { document.getElementById(id).style.display = ''; }
function hide(id) { document.getElementById(id).style.display = 'none'; }

// ── Copy Script ───────────────────────────────
function copyScript() {
  if (!window._rawScript) return;
  navigator.clipboard.writeText(window._rawScript).then(() => {
    showToast('✅ Script copied to clipboard!');
    document.getElementById('copyBtn').textContent = '✅ Copied!';
    setTimeout(() => { document.getElementById('copyBtn').textContent = '📋 Copy'; }, 2000);
  });
}

function copyMusicBrief() {
  if (!window._rawMusicBrief) return;
  navigator.clipboard.writeText(window._rawMusicBrief).then(() => {
    showToast('✅ Music brief copied to clipboard!');
    document.getElementById('copyBriefBtn').textContent = '✅ Copied!';
    setTimeout(() => { document.getElementById('copyBriefBtn').textContent = '📋 Copy Brief'; }, 2000);
  });
}

// ── Toast ─────────────────────────────────────
function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.className = 'toast show';
  if (type === 'error') {
    toast.style.background = 'rgba(239,68,68,0.2)';
    toast.style.borderColor = '#ef4444';
    toast.style.color = '#ef4444';
  } else {
    toast.style.background = 'rgba(16,185,129,0.2)';
    toast.style.borderColor = '#10b981';
    toast.style.color = '#10b981';
  }
  setTimeout(() => { toast.className = 'toast'; }, 3000);
}

// ── Tab Switching ─────────────────────────────
function switchTab(tab) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelector(`.tab-btn[data-tab="${tab}"]`).classList.add('active');

  if (tab === 'scripts') {
    document.getElementById('tabScripts').style.display = '';
    document.getElementById('tabMusic').style.display = 'none';
  } else {
    document.getElementById('tabScripts').style.display = 'none';
    document.getElementById('tabMusic').style.display = '';
    // Render fusion grid on first visit
    if (!window._fusionGridRendered) {
      renderFusionGrid();
      window._fusionGridRendered = true;
    }
  }
}

// ── Music Generation ──────────────────────────
let selectedFusion = 'auto';
let selectedRaga = 'yaman';

const FUSIONS = [
  { key: 'auto', name: 'Auto Optimized', icon: 'cpu', desc: 'AI-determined best fit' },
  { key: 'lo_fi_indian', name: 'Lo-fi Indian', icon: 'headphones', desc: 'Subtle tabla & chill beats' },
  { key: 'trap_desi', name: 'Desi Trap', icon: 'zap', desc: 'Urban 808 & dhol peaks' },
  { key: 'classical_electronic', name: 'Classical EDM', icon: 'activity', desc: 'Sitar & modern synthesis' },
  { key: 'bollywood_pop', name: 'Bollywood Pop', icon: 'music', desc: 'Mainstream appeal' },
  { key: 'ambient_indian', name: 'Ambient', icon: 'wind', desc: 'Tanpura & atmospheric pads' },
  { key: 'folk_modern', name: 'Folk Remix', icon: 'layers', desc: 'Traditional dhol & bass' },
  { key: 'qawwali_edm', name: 'Qawwali EDM', icon: 'moon', desc: 'Spiritual focus & club drive' },
  { key: 'south_indian_fusion', name: 'South Fusion', icon: 'sun', desc: 'Carnatic veena & dynamic beats' },
];

const RAGA_NAMES = {
  yaman: 'Yaman', bhairav: 'Bhairav', des: 'Des', pahadi: 'Pahadi',
  bihag: 'Bihag', khamaj: 'Khamaj', malkauns: 'Malkauns', bhimpalasi: 'Bhimpalasi',
};

// Mood → raga mapping (matches backend)
const MOOD_RAGAS = {
  emotional: ['bhimpalasi', 'yaman', 'des'],
  energetic: ['pahadi', 'khamaj'],
  humorous: ['khamaj', 'pahadi'],
  inspirational: ['des', 'bhairav', 'yaman'],
  elegant: ['yaman', 'bihag', 'malkauns'],
  informative: ['yaman', 'bhimpalasi'],
};

// Mood → good fusion mapping
const MOOD_FUSIONS = {
  emotional: ['ambient_indian', 'classical_electronic'],
  energetic: ['trap_desi', 'bollywood_pop', 'folk_modern'],
  humorous: ['bollywood_pop', 'lo_fi_indian'],
  inspirational: ['classical_electronic', 'folk_modern'],
  elegant: ['ambient_indian', 'classical_electronic', 'south_indian_fusion'],
  informative: ['lo_fi_indian', 'ambient_indian'],
};

// Fusion → instrument labels
const FUSION_INSTRUMENTS = {
  lo_fi_indian: ['Sitar', 'Tabla', 'Tanpura'],
  trap_desi: ['Dhol', 'Tabla', '808'],
  classical_electronic: ['Sitar', 'Santoor', 'Tabla', 'Synth'],
  bollywood_pop: ['Dhol', 'Harmonium', 'Bansuri'],
  ambient_indian: ['Tanpura', 'Bansuri', 'Santoor'],
  folk_modern: ['Dhol', 'Harmonium', 'Shehnai'],
  qawwali_edm: ['Harmonium', 'Tabla', 'Tanpura'],
  south_indian_fusion: ['Veena', 'Mridangam', 'Bansuri'],
};

function renderFusionGrid() {
  const grid = document.getElementById('fusionGrid');
  grid.innerHTML = FUSIONS.map(f => `
    <button class="lang-btn ${f.key === selectedFusion ? 'active' : ''}"
            id="fusion-${f.key}"
            onclick="selectFusion('${f.key}')">
      <span class="lang-native">
        <i data-lucide="${f.icon}" class="icon-sm" style="margin-right:8px"></i>
        ${f.name}
      </span>
      <span class="lang-name">${f.desc}</span>
    </button>
  `).join('');
  if (window.lucide) window.lucide.createIcons();
}

function selectFusion(key) {
  selectedFusion = key;
  document.querySelectorAll('#fusionGrid .lang-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById(`fusion-${key}`);
  if (btn) btn.classList.add('active');
}

// ── Play Music ────────────────────────────────
function playMusic() {
  const tone = document.getElementById('musicTone').value;
  const bpm = parseInt(document.getElementById('musicBpm').value);
  const duration = parseInt(document.getElementById('musicDuration').value);

  // Auto-select raga from mood
  const ragas = MOOD_RAGAS[tone] || MOOD_RAGAS.emotional;
  selectedRaga = ragas[Math.floor(Math.random() * ragas.length)];

  // Auto-select fusion if 'auto'
  let fusion = selectedFusion;
  if (fusion === 'auto') {
    const fusions = MOOD_FUSIONS[tone] || MOOD_FUSIONS.emotional;
    fusion = fusions[Math.floor(Math.random() * fusions.length)];
  }

  // Get instrument names
  const instruments = FUSION_INSTRUMENTS[fusion] || ['🎸 Sitar', '🥁 Tabla', '🕉️ Tanpura'];
  const fusionInfo = FUSIONS.find(f => f.key === fusion) || FUSIONS[3]; // fallback to Classical EDM

  // Update player UI
  hide('musicOutputEmpty');
  show('musicPlayer');

  document.getElementById('playerTitle').textContent = `${RAGA_NAMES[selectedRaga]} — ${fusionInfo.name}`;
  document.getElementById('playerRaga').textContent = RAGA_NAMES[selectedRaga];
  document.getElementById('playerFusion').textContent = fusionInfo.name;
  document.getElementById('playerBpm').textContent = `${bpm} BPM`;
  document.getElementById('playerStatus').textContent = 'Live Playback';

  // Instrument badges
  document.getElementById('playerInstruments').innerHTML =
    instruments.map(i => `<span class="instrument-badge">${i}</span>`).join('');

  // Duration display
  const mins = Math.floor(duration / 60);
  const secs = duration % 60;
  document.getElementById('progressTotal').textContent = `${mins}:${secs.toString().padStart(2, '0')}`;

  // Update layer indicators
  const hasPercussion = ['trap_desi', 'bollywood_pop', 'folk_modern', 'qawwali_edm', 'classical_electronic', 'south_indian_fusion'].includes(fusion);
  const hasBeat = ['trap_desi', 'bollywood_pop', 'folk_modern', 'qawwali_edm'].includes(fusion);
  document.getElementById('layerTanpura').className = 'layer-chip active';
  document.getElementById('layerMelody').className = 'layer-chip active';
  document.getElementById('layerTabla').className = hasPercussion ? 'layer-chip active' : 'layer-chip';
  document.getElementById('layerBeat').className = hasBeat ? 'layer-chip active' : 'layer-chip';
  document.getElementById('layerPad').className = 'layer-chip active';

  // Toggle buttons
  document.getElementById('musicPlayBtn').style.display = 'none';
  document.getElementById('musicStopBtn').style.display = '';

  // Play audio
  window.indianMusic.play({
    raga: selectedRaga,
    fusion: fusion,
    bpm: bpm,
    duration: duration,
  });

  // Start visualizer + progress
  startVisualizer();
  startProgress(duration);

  // Auto-reset when done
  window._musicAutoStop = setTimeout(() => {
    stopMusic();
  }, (duration + 1) * 1000);

  showToast(`🎵 Playing Raga ${RAGA_NAMES[selectedRaga]} — ${fusionInfo.name}`);
}

function stopMusic() {
  window.indianMusic.stop();
  clearTimeout(window._musicAutoStop);
  stopVisualizer();
  stopProgress();

  document.getElementById('musicPlayBtn').style.display = '';
  document.getElementById('musicStopBtn').style.display = 'none';
  document.getElementById('playerStatus').textContent = 'Stopped';

  // Reset progress
  document.getElementById('progressFill').style.width = '0%';
  document.getElementById('progressTime').textContent = '0:00';
}

function setMusicVolume(val) {
  window.indianMusic.setVolume(val / 100);
}

// ── Waveform Visualizer ───────────────────────
let vizAnimFrame = null;

function startVisualizer() {
  const canvas = document.getElementById('waveformCanvas');
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.offsetWidth * 2;
  canvas.height = canvas.offsetHeight * 2;
  ctx.scale(2, 2);

  const w = canvas.offsetWidth;
  const h = canvas.offsetHeight;

  // If we have an audio context with analyser, use real data
  let analyser = null;
  let dataArray = null;
  if (window.indianMusic.ctx) {
    try {
      analyser = window.indianMusic.ctx.createAnalyser();
      analyser.fftSize = 256;
      window.indianMusic.masterGain.connect(analyser);
      dataArray = new Uint8Array(analyser.frequencyBinCount);
    } catch (e) { analyser = null; }
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);

    if (analyser && dataArray) {
      analyser.getByteTimeDomainData(dataArray);
    }

    const bars = 64;
    const barW = w / bars;
    const gradient = ctx.createLinearGradient(0, 0, w, 0);
    gradient.addColorStop(0, '#fde047');
    gradient.addColorStop(0.5, '#fbbf24');
    gradient.addColorStop(1, '#b8860b');

    for (let i = 0; i < bars; i++) {
      let val;
      if (dataArray) {
        const idx = Math.floor(i * dataArray.length / bars);
        val = (dataArray[idx] - 128) / 128;
      } else {
        val = Math.sin(Date.now() / 200 + i * 0.3) * 0.5;
      }

      const barH = Math.abs(val) * h * 0.8 + 2;
      const x = i * barW;
      const y = (h - barH) / 2;

      ctx.fillStyle = gradient;
      ctx.globalAlpha = 0.6 + Math.abs(val) * 0.4;
      ctx.beginPath();
      ctx.roundRect(x + 1, y, barW - 2, barH, 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;

    vizAnimFrame = requestAnimationFrame(draw);
  }

  draw();
}

function stopVisualizer() {
  if (vizAnimFrame) {
    cancelAnimationFrame(vizAnimFrame);
    vizAnimFrame = null;
  }
  // Clear canvas
  const canvas = document.getElementById('waveformCanvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
}

// ── Progress Bar ──────────────────────────────
let progressInterval = null;

function startProgress(duration) {
  const startTime = Date.now();
  const fill = document.getElementById('progressFill');
  const timeEl = document.getElementById('progressTime');

  progressInterval = setInterval(() => {
    const elapsed = (Date.now() - startTime) / 1000;
    const pct = Math.min((elapsed / duration) * 100, 100);
    fill.style.width = pct + '%';

    const mins = Math.floor(elapsed / 60);
    const secs = Math.floor(elapsed % 60);
    timeEl.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;

    if (elapsed >= duration) {
      clearInterval(progressInterval);
    }
  }, 500);
}

function stopProgress() {
  if (progressInterval) {
    clearInterval(progressInterval);
    progressInterval = null;
  }
}

// ── Music Brief Generation ─────────────────────
async function generateMusicBrief() {
  const brandName = document.getElementById('musicBrand').value.trim();
  const theme = document.getElementById('musicTheme').value.trim();
  const industry = document.getElementById('musicIndustry').value;
  const tone = document.getElementById('musicTone').value;
  const festival = document.getElementById('musicFestival').value;
  const adFormat = document.getElementById('musicFormat').value;

  const btn = document.getElementById('musicBriefBtn');
  const originalText = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = '<span class="loading-spinner-xs"></span> Generating Brief...';

  // Prepare UI
  hide('musicOutputEmpty');
  show('musicPlayer');
  hide('briefResult');

  try {
    const payload = {
      ad_format: adFormat,
      tone: tone,
      industry: industry,
      brand_name: brandName || 'Generic',
      theme: theme || 'Modern Indian',
      festival: festival,
      fusion_style: selectedFusion,
      language: selectedLanguage,
    };

    const res = await fetch(`${API_BASE}/music/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Music brief generation failed');
    }

    const data = await res.json();

    // Update UI with brief
    show('briefResult');
    document.getElementById('briefOutput').textContent = data.brief;
    window._rawMusicBrief = data.brief;

    // Also update global player meta if not already playing
    if (!window.indianMusic.isPlaying) {
      document.getElementById('playerTitle').textContent = data.title;
      document.getElementById('playerRaga').textContent = data.raga;
      document.getElementById('playerFusion').textContent = data.fusion_style;
      document.getElementById('playerBpm').textContent = data.tempo;

      // Instrument badges
      document.getElementById('playerInstruments').innerHTML =
        data.instruments.map(i => `<span class="instrument-badge">${i}</span>`).join('');
    }

    showToast('✨ Professional Music Brief Generated!');

  } catch (err) {
    showToast(`⚠️ ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = originalText;
  }
}
