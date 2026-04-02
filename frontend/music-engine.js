/**
 * MetaCraft AI — Indian Music Synthesizer Engine
 * Web Audio API-based engine for playing Indian raga melodies,
 * tabla beats, tanpura drone, and modern fusion layers.
 */

class IndianMusicEngine {
    constructor() {
        this.ctx = null;
        this.isPlaying = false;
        this.masterGain = null;
        this.layers = {};
        this.timers = [];
        this.bpm = 100;
        this.currentRaga = 'yaman';
        this.currentFusion = 'classical_electronic';
        this.duration = 30; // seconds

        // Indian note frequencies (Sa = C4 = 261.63 Hz, using just intonation)
        this.SA = 261.63;
        this.NOTE_RATIOS = {
            'Sa': 1, 'Re_komal': 16 / 15, 'Re': 9 / 8, 'Ga_komal': 6 / 5, 'Ga': 5 / 4,
            'Ma': 4 / 3, 'Ma_tivra': 45 / 32, 'Pa': 3 / 2, 'Dha_komal': 8 / 5, 'Dha': 5 / 3,
            'Ni_komal': 9 / 5, 'Ni': 15 / 8, 'Sa2': 2, 'Re2': 9 / 4, 'Ga2': 5 / 2,
        };

        // Raga definitions (aroha - ascending notes)
        this.RAGAS = {
            yaman: ['Sa', 'Re', 'Ga', 'Ma_tivra', 'Pa', 'Dha', 'Ni', 'Sa2'],
            bhairav: ['Sa', 'Re_komal', 'Ga', 'Ma', 'Pa', 'Dha_komal', 'Ni', 'Sa2'],
            des: ['Sa', 'Re', 'Ma', 'Pa', 'Ni', 'Sa2'],
            pahadi: ['Sa', 'Re', 'Ga', 'Pa', 'Dha', 'Sa2'],
            bihag: ['Sa', 'Ga', 'Ma', 'Pa', 'Ni', 'Sa2'],
            khamaj: ['Sa', 'Re', 'Ga', 'Ma', 'Pa', 'Dha', 'Ni_komal', 'Sa2'],
            malkauns: ['Sa', 'Ga_komal', 'Ma', 'Dha_komal', 'Ni_komal', 'Sa2'],
            bhimpalasi: ['Sa', 'Re', 'Ga_komal', 'Ma', 'Pa', 'Ni', 'Dha', 'Pa'],
        };

        // Tabla patterns (taal) — Teentaal (16 beats)
        this.TABLA_PATTERNS = {
            teentaal: {
                dha: [0, 4, 8, 12], // Sam, Khali positions
                ti: [2, 6, 10, 14],
                na: [1, 3, 9, 11],
                tin: [5, 7, 13, 15],
            },
            keherwa: { // 8 beats — faster, dance-like
                dha: [0, 4],
                ge: [1, 5],
                na: [2, 6],
                ti: [3, 7],
            },
        };
    }

    init() {
        if (!this.ctx) {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
            this.masterGain = this.ctx.createGain();
            this.masterGain.gain.value = 0.7;
            this.masterGain.connect(this.ctx.destination);
        }
        if (this.ctx.state === 'suspended') this.ctx.resume();
    }

    getFreq(note) {
        return this.SA * (this.NOTE_RATIOS[note] || 1);
    }

    // ── Tanpura Drone Layer ─────────────────────
    startTanpura() {
        const gain = this.ctx.createGain();
        gain.gain.value = 0.12;
        gain.connect(this.masterGain);

        const notes = [this.SA, this.SA * 1.5, this.SA * 2, this.SA * 0.5]; // Sa, Pa, Sa(high), Sa(low)
        const oscillators = notes.map((freq, i) => {
            const osc = this.ctx.createOscillator();
            osc.type = 'sine';
            osc.frequency.value = freq;

            // Subtle vibrato for organic feel
            const lfo = this.ctx.createOscillator();
            lfo.frequency.value = 0.3 + i * 0.1;
            const lfoGain = this.ctx.createGain();
            lfoGain.gain.value = 1.5;
            lfo.connect(lfoGain);
            lfoGain.connect(osc.frequency);
            lfo.start();

            // Filter for warmth
            const filter = this.ctx.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.value = 800 + i * 200;
            filter.Q.value = 1;
            osc.connect(filter);
            filter.connect(gain);
            osc.start();

            return { osc, lfo };
        });

        this.layers.tanpura = { gain, oscillators };
    }

    // ── Melodic Sitar/Bansuri Layer ─────────────
    startMelody() {
        const ragaNotes = this.RAGAS[this.currentRaga] || this.RAGAS.yaman;
        const beatDuration = 60 / this.bpm;
        let time = this.ctx.currentTime + 0.5;

        const gain = this.ctx.createGain();
        gain.gain.value = 0.25;
        gain.connect(this.masterGain);

        // Reverb-like delay
        const delay = this.ctx.createDelay(0.5);
        delay.delayTime.value = 0.15;
        const delayGain = this.ctx.createGain();
        delayGain.gain.value = 0.3;
        delay.connect(delayGain);
        delayGain.connect(gain);

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.value = 2000;
        filter.Q.value = 3;
        filter.connect(gain);
        filter.connect(delay);

        // Generate melodic phrases
        const totalBeats = Math.floor(this.duration / beatDuration);
        const oscillators = [];

        for (let i = 0; i < totalBeats; i++) {
            // Musical phrasing — sometimes rest, sometimes hold
            if (Math.random() < 0.15) { time += beatDuration; continue; } // rest

            const noteIdx = this.generateMelodicIndex(ragaNotes.length, i, totalBeats);
            const freq = this.getFreq(ragaNotes[noteIdx]);
            const noteDur = beatDuration * (Math.random() < 0.3 ? 2 : 1); // Sometimes longer notes

            const osc = this.ctx.createOscillator();
            // Alternate between sitar-like and flute-like timbres
            osc.type = i % 4 < 2 ? 'sawtooth' : 'triangle';
            osc.frequency.value = freq;

            const noteGain = this.ctx.createGain();
            // Indian-style attack — slight bend into the note (meend)
            noteGain.gain.setValueAtTime(0, time);
            noteGain.gain.linearRampToValueAtTime(0.8, time + 0.05);
            noteGain.gain.exponentialRampToValueAtTime(0.3, time + noteDur * 0.5);
            noteGain.gain.linearRampToValueAtTime(0.001, time + noteDur);

            // Slight pitch bend (meend) — signature Indian ornament
            if (Math.random() < 0.4 && noteIdx > 0) {
                const prevFreq = this.getFreq(ragaNotes[Math.max(0, noteIdx - 1)]);
                osc.frequency.setValueAtTime(prevFreq, time);
                osc.frequency.exponentialRampToValueAtTime(freq, time + 0.08);
            }

            // Gamak (oscillation) on some notes
            if (Math.random() < 0.2) {
                const vibLfo = this.ctx.createOscillator();
                vibLfo.frequency.value = 5 + Math.random() * 3;
                const vibGain = this.ctx.createGain();
                vibGain.gain.value = freq * 0.02;
                vibLfo.connect(vibGain);
                vibGain.connect(osc.frequency);
                vibLfo.start(time);
                vibLfo.stop(time + noteDur);
            }

            osc.connect(noteGain);
            noteGain.connect(filter);
            osc.start(time);
            osc.stop(time + noteDur + 0.01);
            oscillators.push(osc);

            time += noteDur;
        }

        this.layers.melody = { gain, oscillators };
    }

    generateMelodicIndex(length, beat, total) {
        // Create musical phrases — ascending, descending, and pakad patterns
        const phase = (beat / total) * Math.PI * 4;
        const base = Math.sin(phase) * 0.5 + 0.5; // 0 to 1
        let idx = Math.floor(base * (length - 1));

        // Add some randomness for natural feel
        idx += Math.floor(Math.random() * 3) - 1;
        return Math.max(0, Math.min(length - 1, idx));
    }

    // ── Tabla / Percussion Layer ────────────────
    startTabla() {
        const beatDuration = 60 / this.bpm / 2; // eighth notes for tabla
        const pattern = this.bpm > 120 ? this.TABLA_PATTERNS.keherwa : this.TABLA_PATTERNS.teentaal;
        const patternLength = this.bpm > 120 ? 8 : 16;

        const gain = this.ctx.createGain();
        gain.gain.value = 0.35;
        gain.connect(this.masterGain);

        let time = this.ctx.currentTime + 0.5;
        const totalSteps = Math.floor(this.duration / beatDuration);

        for (let i = 0; i < totalSteps; i++) {
            const pos = i % patternLength;

            // Dha — low bass hit (bayan)
            if (pattern.dha.includes(pos)) {
                this.scheduleTablaHit(time, 80, 0.15, 0.7, gain, 'dha');
            }
            // Na/Ti — high sharp hit (dayan)
            if ((pattern.na && pattern.na.includes(pos)) || (pattern.ti && pattern.ti.includes(pos))) {
                this.scheduleTablaHit(time, 300 + Math.random() * 100, 0.08, 0.5, gain, 'na');
            }
            // Tin — mid crackle
            if (pattern.tin && pattern.tin.includes(pos)) {
                this.scheduleTablaHit(time, 200, 0.1, 0.4, gain, 'tin');
            }
            // Ge — soft bass
            if (pattern.ge && pattern.ge.includes(pos)) {
                this.scheduleTablaHit(time, 60, 0.12, 0.3, gain, 'ge');
            }

            time += beatDuration;
        }

        this.layers.tabla = { gain };
    }

    scheduleTablaHit(time, freq, duration, volume, destination, type) {
        const osc = this.ctx.createOscillator();
        const hitGain = this.ctx.createGain();

        if (type === 'dha' || type === 'ge') {
            // Bass drum — sine with pitch drop
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq * 2, time);
            osc.frequency.exponentialRampToValueAtTime(freq, time + 0.04);
            hitGain.gain.setValueAtTime(volume, time);
            hitGain.gain.exponentialRampToValueAtTime(0.001, time + duration);
        } else {
            // Sharp hit — noise-like via high harmonics
            osc.type = 'square';
            osc.frequency.setValueAtTime(freq, time);
            osc.frequency.exponentialRampToValueAtTime(freq * 0.5, time + duration);
            hitGain.gain.setValueAtTime(volume * 0.6, time);
            hitGain.gain.exponentialRampToValueAtTime(0.001, time + duration * 0.7);
        }

        // Add a noise burst for attack
        const noise = this.createNoiseNode(duration * 0.5);
        const noiseGain = this.ctx.createGain();
        noiseGain.gain.setValueAtTime(volume * 0.15, time);
        noiseGain.gain.exponentialRampToValueAtTime(0.001, time + 0.03);
        noise.connect(noiseGain);
        noiseGain.connect(destination);
        noise.start(time);
        noise.stop(time + duration);

        osc.connect(hitGain);
        hitGain.connect(destination);
        osc.start(time);
        osc.stop(time + duration + 0.01);
    }

    createNoiseNode(duration) {
        const bufferSize = this.ctx.sampleRate * Math.max(duration, 0.1);
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        const source = this.ctx.createBufferSource();
        source.buffer = buffer;
        return source;
    }

    // ── Modern Beat Layer ───────────────────────
    startModernBeat() {
        const beatDuration = 60 / this.bpm;
        const gain = this.ctx.createGain();
        gain.gain.value = 0.2;
        gain.connect(this.masterGain);

        let time = this.ctx.currentTime + 0.5;
        const totalBeats = Math.floor(this.duration / beatDuration);

        for (let i = 0; i < totalBeats; i++) {
            const beatPos = i % 4;

            // Kick on 1 and 3
            if (beatPos === 0 || beatPos === 2) {
                this.scheduleKick(time, gain);
            }

            // Hi-hat on every beat (softer on off-beats)
            this.scheduleHiHat(time, beatPos % 2 === 0 ? 0.3 : 0.15, gain);

            // Sub bass hit on 1
            if (beatPos === 0) {
                const sub = this.ctx.createOscillator();
                sub.type = 'sine';
                sub.frequency.value = 45;
                const subGain = this.ctx.createGain();
                subGain.gain.setValueAtTime(0.4, time);
                subGain.gain.exponentialRampToValueAtTime(0.001, time + beatDuration * 0.8);
                sub.connect(subGain);
                subGain.connect(gain);
                sub.start(time);
                sub.stop(time + beatDuration);
            }

            time += beatDuration;
        }

        this.layers.modernBeat = { gain };
    }

    scheduleKick(time, dest) {
        const osc = this.ctx.createOscillator();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(150, time);
        osc.frequency.exponentialRampToValueAtTime(40, time + 0.1);
        const g = this.ctx.createGain();
        g.gain.setValueAtTime(0.6, time);
        g.gain.exponentialRampToValueAtTime(0.001, time + 0.2);
        osc.connect(g);
        g.connect(dest);
        osc.start(time);
        osc.stop(time + 0.25);
    }

    scheduleHiHat(time, vol, dest) {
        const noise = this.createNoiseNode(0.05);
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'highpass';
        filter.frequency.value = 7000;
        const g = this.ctx.createGain();
        g.gain.setValueAtTime(vol, time);
        g.gain.exponentialRampToValueAtTime(0.001, time + 0.05);
        noise.connect(filter);
        filter.connect(g);
        g.connect(dest);
        noise.start(time);
        noise.stop(time + 0.06);
    }

    // ── Pad / Atmosphere Layer ──────────────────
    startPad() {
        const ragaNotes = this.RAGAS[this.currentRaga] || this.RAGAS.yaman;
        const gain = this.ctx.createGain();
        gain.gain.value = 0.08;
        gain.connect(this.masterGain);

        // Chord pad using 3 notes from the raga
        const chordNotes = [ragaNotes[0], ragaNotes[2], ragaNotes[4]];
        chordNotes.forEach(note => {
            const osc = this.ctx.createOscillator();
            osc.type = 'sine';
            osc.frequency.value = this.getFreq(note) * 0.5; // Lower octave for pad
            const filter = this.ctx.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.value = 400;
            filter.Q.value = 0.5;

            // Slow LFO for movement
            const lfo = this.ctx.createOscillator();
            lfo.frequency.value = 0.1;
            const lfoGain = this.ctx.createGain();
            lfoGain.gain.value = 50;
            lfo.connect(lfoGain);
            lfoGain.connect(filter.frequency);
            lfo.start();

            osc.connect(filter);
            filter.connect(gain);
            osc.start();
        });

        this.layers.pad = { gain };
    }

    // ── Main Controls ───────────────────────────
    play(config = {}) {
        this.stop(); // Stop any existing playback
        this.init();

        this.currentRaga = config.raga || 'yaman';
        this.currentFusion = config.fusion || 'classical_electronic';
        this.bpm = config.bpm || 100;
        this.duration = config.duration || 30;

        // Fade in
        this.masterGain.gain.setValueAtTime(0, this.ctx.currentTime);
        this.masterGain.gain.linearRampToValueAtTime(0.7, this.ctx.currentTime + 1);

        // Start layers based on fusion style
        this.startTanpura();
        this.startPad();
        this.startMelody();

        // Add percussion based on fusion
        if (['trap_desi', 'bollywood_pop', 'folk_modern', 'qawwali_edm'].includes(this.currentFusion)) {
            this.startTabla();
            this.startModernBeat();
        } else if (['classical_electronic', 'south_indian_fusion'].includes(this.currentFusion)) {
            this.startTabla();
        } else if (['lo_fi_indian', 'ambient_indian'].includes(this.currentFusion)) {
            // Lighter percussion with slower tempo
            this.bpm = Math.min(this.bpm, 85);
            this.startTabla();
        }

        this.isPlaying = true;

        // Auto-stop with fade-out
        const fadeOutTime = this.ctx.currentTime + this.duration - 2;
        this.timers.push(setTimeout(() => {
            if (this.masterGain && this.isPlaying) {
                this.masterGain.gain.linearRampToValueAtTime(0, this.ctx.currentTime + 2);
                this.timers.push(setTimeout(() => this.stop(), 2200));
            }
        }, (this.duration - 2) * 1000));
    }

    stop() {
        this.isPlaying = false;
        this.timers.forEach(t => clearTimeout(t));
        this.timers = [];

        if (this.ctx) {
            // Stop all oscillators
            Object.values(this.layers).forEach(layer => {
                if (layer.oscillators) {
                    layer.oscillators.forEach(o => {
                        try { if (o.osc) { o.osc.stop(); o.lfo.stop(); } else { o.stop(); } } catch (e) { }
                    });
                }
                if (layer.gain) {
                    try { layer.gain.disconnect(); } catch (e) { }
                }
            });
            this.layers = {};

            // Close and recreate context for clean state
            try { this.ctx.close(); } catch (e) { }
            this.ctx = null;
            this.masterGain = null;
        }
    }

    setVolume(vol) {
        if (this.masterGain) {
            this.masterGain.gain.linearRampToValueAtTime(vol, this.ctx.currentTime + 0.1);
        }
    }
}

// Expose globally
window.indianMusic = new IndianMusicEngine();
