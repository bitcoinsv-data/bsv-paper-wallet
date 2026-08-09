# Builds bsv-paper-wallet.html: the official iancoleman/bip39 standalone file
# (vendored, untouched) + a BSV-only guided UI layered on top.
#
# The UI layer performs NO cryptography of its own: it drives the hidden
# upstream page (coin pinned to BSV, strength, BIP38 fields) and reads its
# outputs. QR codes are rendered with the kjua library already bundled inside
# the upstream file. The page makes zero network requests: fonts fall back to
# system faces and the BSV logo is an inline data URI.
#
# Usage:  python build.py   ->  bsv-paper-wallet.html
import io

SRC = 'vendor/bip39-standalone.html'
OUT = 'bsv-paper-wallet.html'

patch = r'''
<!-- ===== SIMPLE BSV PAPER WALLET MODE (local addition; upstream generation code above is untouched) ===== -->
<style id="simple-mode-style">
:root {
  --pagebg:#F8FAFC; --panel:#ffffff; --page:#F8FAFC;
  --ink:#0F172A; --slate7:#334155; --slate6:#475569; --slate5:#64748B; --slate4:#94A3B8;
  --line:#E2E8F0; --line2:#F1F5F9; --linemid:#CBD5E1;
  --indigo:#4F46E5; --indigo2:#6366F1; --indigolight:#EEF2FF; --indigodark:#4338CA;
  --green:#10B981; --greendark:#047857; --greenpale:#ECFDF5; --greenline:#A7F3D0; --greenlite:#F0FDF4; --greenbd:#86EFAC;
  --red:#EF4444; --reddark:#B91C1C; --redpale:#FEF2F2; --redline:#FECACA; --redtxt:#991B1B;
  --rose:#F43F5E; --rosedark:#BE123C; --rosepale:#FFF1F2;
  --amberpale:#FFFBEB; --amberline:#FDE68A; --ambertxt:#92400E; --amberdot:#F59E0B;
  --sans:"IBM Plex Sans","Segoe UI",Helvetica,Arial,sans-serif;
  --mono:"IBM Plex Mono",Consolas,"Courier New",monospace;
}
/* automatic dark mode, unless the user forced light with the header toggle */
@media (prefers-color-scheme: dark) { :root:not(.sp-light) {
  --pagebg:#020617; --panel:#0F172A; --page:#1E293B;
  --ink:#F8FAFC; --slate7:#CBD5E1; --slate6:#CBD5E1; --slate5:#94A3B8; --slate4:#64748B;
  --line:#334155; --line2:#293548; --linemid:#475569;
  --indigo:#6366F1; --indigo2:#818CF8; --indigolight:rgba(99,102,241,.15); --indigodark:#A5B4FC;
  --greendark:#34D399; --greenpale:rgba(16,185,129,.1); --greenline:rgba(16,185,129,.25);
  --greenlite:rgba(16,185,129,.12); --greenbd:rgba(16,185,129,.35);
  --reddark:#F87171; --redpale:rgba(239,68,68,.1); --redline:rgba(239,68,68,.25); --redtxt:#F87171;
  --amberpale:rgba(245,158,11,.1); --amberline:rgba(245,158,11,.25); --ambertxt:#FBBF24;
} }
/* forced dark via the header toggle */
:root.sp-dark {
  --pagebg:#020617; --panel:#0F172A; --page:#1E293B;
  --ink:#F8FAFC; --slate7:#CBD5E1; --slate6:#CBD5E1; --slate5:#94A3B8; --slate4:#64748B;
  --line:#334155; --line2:#293548; --linemid:#475569;
  --indigo:#6366F1; --indigo2:#818CF8; --indigolight:rgba(99,102,241,.15); --indigodark:#A5B4FC;
  --greendark:#34D399; --greenpale:rgba(16,185,129,.1); --greenline:rgba(16,185,129,.25);
  --greenlite:rgba(16,185,129,.12); --greenbd:rgba(16,185,129,.35);
  --reddark:#F87171; --redpale:rgba(239,68,68,.1); --redline:rgba(239,68,68,.25); --redtxt:#F87171;
  --amberpale:rgba(245,158,11,.1); --amberline:rgba(245,158,11,.25); --ambertxt:#FBBF24;
}
body { background:var(--pagebg); color:var(--ink); transition:background .3s ease, color .3s ease; }
body.sp-ready > #simple-panel { display:block !important; }
body.sp-ready > #advanced-wrap { display:block !important; }
body.sp-ready::before { content:none !important; }
#advanced-wrap.sp-collapsed .feedback-container { display:none !important; }
#advanced-wrap.sp-collapsed { height:0; overflow:hidden; margin:0; padding:0; border:none; }

#simple-panel { font-family:var(--sans); color:var(--ink); max-width:920px; margin:0 auto; padding:28px 14px 60px; }
#simple-panel button { font-family:var(--sans); }
#simple-panel button:active { transform:translateY(1px); }

/* ---- app panel ---- */
.sp-app { background:var(--panel); border:1px solid var(--line); border-radius:24px;
  box-shadow:0 12px 32px -12px rgba(0,0,0,0.08); overflow:hidden; }
.sp-apphead { display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap;
  padding:20px 32px; border-bottom:1px solid var(--line2); }
.sp-appname { font:700 17px var(--sans); letter-spacing:.2px; color:var(--ink); }
.sp-appver { font:500 13px var(--mono); color:var(--slate4); margin-left:10px; }
#sp-theme-btn { background:var(--panel); border:1px solid var(--line); border-radius:8px;
  padding:6px 10px; font-size:15px; cursor:pointer; line-height:1; }
#sp-theme-btn:hover { background:var(--line2); }
.sp-pill { display:flex; align-items:center; gap:8px; border-radius:999px; padding:6px 14px 6px 12px; }
.sp-pill .sp-dot { width:8px; height:8px; border-radius:50%; }
.sp-pill span:last-child { font:600 11px var(--mono); letter-spacing:1.5px; }
.sp-pill.off { background:var(--greenpale); border:1px solid var(--greenline); }
.sp-pill.off .sp-dot { background:var(--green); box-shadow:0 0 6px rgba(16,185,129,.5); }
.sp-pill.off span:last-child { color:var(--greendark); }
.sp-pill.on { background:var(--redpale); border:1px solid var(--redline); }
.sp-pill.on .sp-dot { background:var(--red); box-shadow:0 0 6px rgba(239,68,68,.5); }
.sp-pill.on span:last-child { color:var(--reddark); }
.sp-pill.warn { background:var(--amberpale); border:1px solid var(--amberline); }
.sp-pill.warn .sp-dot { background:var(--amberdot); box-shadow:0 0 6px rgba(245,158,11,.5); }
.sp-pill.warn span:last-child { color:var(--ambertxt); }
#sp-net-banner { display:flex; gap:14px; align-items:flex-start; padding:18px 32px;
  background:var(--redpale); border-bottom:1px solid var(--redline); }
#sp-handheld-banner { display:none; gap:14px; align-items:flex-start; padding:18px 32px;
  background:var(--amberpale); border-bottom:1px solid var(--amberline); }
#sp-handheld-banner .sp-bang { width:24px; height:24px; flex:0 0 24px; border-radius:50%;
  background:var(--amberdot); color:#fff; font:700 14px var(--sans); display:flex;
  align-items:center; justify-content:center; }
#sp-handheld-banner div:last-child { font:400 14px/1.55 var(--sans); color:var(--ambertxt); }
#sp-net-banner .sp-bang { width:24px; height:24px; flex:0 0 24px; border-radius:50%; background:var(--red);
  color:#fff; font:700 14px var(--sans); display:flex; align-items:center; justify-content:center;
  box-shadow:0 2px 8px rgba(239,68,68,.3); }
#sp-net-banner div:last-child { font:400 14px/1.55 var(--sans); color:var(--redtxt); }
.sp-body { padding:32px; }
@media (max-width:640px){ .sp-body { padding:24px 16px; } }
.sp-hero { font:700 30px/1.2 var(--sans); letter-spacing:-.5px; color:var(--ink); max-width:620px; }
.sp-herosub { font:400 16px/1.6 var(--sans); color:var(--slate6); max-width:660px; margin-top:12px; }
.sp-btcwarn { font-weight:600; color:var(--reddark); }

#sp-dirty { margin-top:20px; display:none; gap:12px; align-items:flex-start; border:1px solid var(--amberline);
  background:var(--amberpale); border-radius:12px; padding:16px; }
#sp-dirty .sp-bang2 { width:22px; height:22px; flex:0 0 22px; border-radius:50%; background:var(--amberdot);
  color:#fff; font:700 13px var(--sans); display:flex; align-items:center; justify-content:center; }
#sp-dirty div:last-child { font:400 14px/1.5 var(--sans); color:var(--ambertxt); }

/* ---- setup card ---- */
.sp-setup { margin-top:32px; border:1px solid var(--line); background:var(--page); border-radius:16px; overflow:hidden; }
.sp-setup-grid { display:grid; grid-template-columns:1fr 1fr; border-bottom:1px solid var(--line); }
@media (max-width:640px){ .sp-setup-grid { grid-template-columns:1fr; } .sp-cell-r { border-right:none !important; border-bottom:1px solid var(--line); } }
.sp-cell { padding:24px; }
.sp-cell-r { border-right:1px solid var(--line); }
.sp-lab { font:600 13px var(--mono); letter-spacing:1.6px; color:var(--slate5); }
.sp-choices { display:flex; gap:12px; margin-top:14px; }
.sp-choice { flex:1; padding:14px 12px; background:var(--panel); border:1px solid var(--line); border-radius:10px;
  cursor:pointer; text-align:left; }
.sp-choice:hover { border-color:var(--linemid); }
.sp-choice b { display:block; font:600 15px var(--sans); color:var(--slate6); }
.sp-choice span { display:block; font:400 12.5px var(--sans); color:var(--slate4); margin-top:4px; }
.sp-choice.sel { background:var(--indigolight); border:2px solid var(--indigo2); padding:13px 11px;
  box-shadow:0 4px 12px rgba(99,102,241,.1); }
.sp-choice.sel b { color:var(--indigodark); }
.sp-choice.sel span { color:var(--indigo2); }
.sp-counter { display:flex; align-items:center; gap:16px; margin-top:14px; flex-wrap:wrap; }
.sp-counterbox { display:flex; align-items:center; background:var(--panel); border:1px solid var(--line);
  border-radius:10px; overflow:hidden; }
.sp-counterbox button { width:48px; height:48px; border:none; background:transparent;
  font:400 24px var(--sans); color:var(--ink); cursor:pointer; }
.sp-counterbox button:hover { background:var(--line2); }
.sp-counterbox button:disabled { opacity:.35; cursor:default; }
#sp-dec { border-right:1px solid var(--line); }
#sp-inc { border-left:1px solid var(--line); }
#sp-count-display { font:600 24px var(--mono); color:var(--indigo); min-width:48px; text-align:center; }
.sp-counter-note { font:400 13px/1.45 var(--sans); color:var(--slate5); max-width:190px; }

.sp-pwrow { padding:24px; border-bottom:1px solid var(--line); background:var(--panel); display:flex; align-items:flex-start; gap:16px; }
.sp-switch { margin-top:2px; width:48px; height:28px; flex:0 0 48px; border-radius:999px; border:none;
  cursor:pointer; padding:0; display:flex; align-items:center; background:var(--linemid); transition:background .2s; }
.sp-switch .sp-knob { width:22px; height:22px; border-radius:50%; background:#fff;
  box-shadow:0 2px 4px rgba(0,0,0,.2); margin-left:4px; transition:margin-left .2s cubic-bezier(.4,0,.2,1); }
.sp-switch.on { background:var(--indigo); }
.sp-switch.on .sp-knob { margin-left:24px; }
.sp-pwmain { flex:1; }
.sp-pwtitle { font:600 15px var(--sans); color:var(--ink); display:flex; align-items:center; gap:12px; flex-wrap:wrap; }
.sp-chip { font:600 10.5px var(--mono); letter-spacing:1.6px; color:var(--indigo); background:var(--indigolight);
  border-radius:4px; padding:4px 10px; }
.sp-pwstate { font:400 14px/1.5 var(--sans); color:var(--slate6); margin-top:6px; max-width:620px; }
#sp-pw-wrap { margin-top:16px; display:none; flex-direction:column; gap:12px; max-width:540px;
  background:var(--page); padding:16px; border-radius:12px; border:1px solid var(--line); }
.sp-pwline { display:flex; gap:12px; align-items:center; }
#sp-bip38-pw, #sp-bip38-pw2 { flex:1; min-width:0; font:500 15px var(--mono); padding:12px 14px;
  border:1px solid var(--linemid); border-radius:8px; background:var(--panel); color:var(--ink); outline:none;
  box-sizing:border-box; width:100%; }
#sp-bip38-pw:focus, #sp-bip38-pw2:focus { border-color:var(--indigo2); box-shadow:0 0 0 3px rgba(99,102,241,.1); }
#sp-bip38-pw2.bad { border-color:var(--red); }
#sp-pw-show { flex:0 0 auto; padding:12px 16px; background:var(--panel); border:1px solid var(--linemid);
  border-radius:8px; font:600 13px var(--sans); color:var(--slate6); cursor:pointer; }
#sp-pw-show:hover { background:var(--line2); }
#sp-pw-mismatch { display:none; font:500 13px var(--sans); color:var(--red); }
.sp-pwnote { font:400 13px/1.5 var(--sans); color:var(--slate5); }
.sp-setup-foot { padding:20px 24px; display:flex; align-items:center; justify-content:space-between;
  gap:24px; flex-wrap:wrap; background:var(--panel); }
#sp-summary { font:500 14px/1.5 var(--sans); color:var(--slate7); max-width:440px; }
#sp-regen-note { font:400 13px var(--sans); color:var(--slate4); margin-top:4px; display:none; }
#sp-generate { background:linear-gradient(135deg, #6366F1, #4F46E5); color:#fff; border:none;
  padding:16px 40px; border-radius:12px; font:600 16px var(--sans); letter-spacing:.3px; cursor:pointer;
  box-shadow:0 8px 16px -4px rgba(79,70,229,.3); transition:all .2s; }
#sp-generate:hover { box-shadow:0 12px 20px -4px rgba(79,70,229,.4); transform:translateY(-2px); }
#simple-status { font:400 14px/1.5 var(--sans); color:var(--slate6); margin:14px 2px 0; min-height:18px; }

/* generating box */
#sp-genbox { display:none; margin-top:40px; border:2px dashed var(--linemid); border-radius:16px;
  background:var(--page); padding:48px 24px; text-align:center; }
#sp-genbox .sp-genhead { font:600 18px var(--sans); color:var(--indigo); display:flex; justify-content:center;
  align-items:center; gap:12px; }
#sp-genbox .sp-spin { width:22px; height:22px; border:3px solid var(--indigolight); border-top-color:var(--indigo);
  border-radius:50%; animation:spspin 1s linear infinite; }
@keyframes spspin { 100% { transform:rotate(360deg); } }
#sp-genbox .sp-gensub { font:400 14px var(--sans); color:var(--slate5); margin-top:12px; }

/* ---- stepper ---- */
#sp-steps { margin-top:40px; display:none; }
.sp-st { display:flex; gap:24px; }
.sp-strail { display:flex; flex-direction:column; align-items:center; width:36px; flex:0 0 36px; }
.sp-snum { width:36px; height:36px; border-radius:50%; background:var(--indigo); color:#fff;
  font:600 16px var(--mono); display:flex; align-items:center; justify-content:center;
  box-shadow:0 4px 10px rgba(79,70,229,.3); transition:all .3s; }
.sp-snum.idle { background:var(--panel); color:var(--slate4); border:2px solid var(--line); box-shadow:none; }
.sp-strail .sp-line { flex:1; width:2px; background:var(--line); margin:8px 0; }
.sp-sbody { flex:1; padding-bottom:40px; min-width:0; transition:opacity .3s; }
.sp-stitle { font:700 20px var(--sans); color:var(--ink); display:flex; align-items:center; gap:12px; flex-wrap:wrap; }
.sp-stitle.gray { color:var(--slate4); }
.sp-ssub { font:400 15px/1.6 var(--sans); color:var(--slate6); margin-top:6px; max-width:620px; }
.sp-ssub.gray { color:var(--slate4); }
.sp-dim { opacity:.5; }

#sp-warn-onscreen { display:none; gap:12px; align-items:center; margin-top:20px; border:1px solid #FCA5A5;
  border-radius:10px; background:var(--redpale); padding:12px 16px; max-width:620px; }
#sp-warn-onscreen .sp-bang3 { width:20px; height:20px; flex:0 0 20px; border-radius:50%; background:var(--red);
  color:#fff; font:700 12px var(--sans); display:flex; align-items:center; justify-content:center; }
#sp-warn-onscreen div:last-child { font:400 13px var(--sans); color:var(--redtxt); }

.sp-secretbox { margin-top:20px; border:1px solid var(--line); border-radius:12px; background:var(--panel);
  overflow:hidden; box-shadow:0 4px 6px -1px rgba(0,0,0,.05); }
.sp-secrethead { display:flex; align-items:center; justify-content:space-between; gap:10px;
  padding:16px 20px; background:var(--page); border-bottom:1px solid var(--line); }
#sp-seedcount { font:600 14px var(--mono); letter-spacing:1.6px; color:var(--indigo); }
#sp-seed-btn { background:var(--panel); border:1px solid var(--linemid); border-radius:8px; color:var(--slate7);
  font:600 13px var(--sans); letter-spacing:.4px; padding:10px 16px; cursor:pointer; }
#sp-seed-btn:hover { background:var(--line2); border-color:var(--slate4); }
#sp-seed-hiddenmsg { padding:48px 20px; text-align:center; font:400 15px/1.6 var(--sans); color:var(--slate5); }
#sp-seed-grid { padding:24px 24px 12px; display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; }
@media (max-width:640px){
  .sp-st { gap:14px; }
  #sp-seed-grid { grid-template-columns:repeat(2,minmax(0,1fr)); padding:16px 14px 8px; gap:8px 10px; }
  .sp-w { gap:7px; }
  .sp-w b { font-size:15px; }
  .sp-alsoline { margin:8px 14px 0; }
  .sp-alsoline b { font-size:14px; }
}
.sp-w { display:flex; align-items:baseline; gap:10px; border-bottom:1px dashed var(--line); padding:8px 4px; min-width:0; }
.sp-w i { font:400 13px var(--mono); font-style:normal; color:var(--slate7); width:20px; text-align:right; flex:0 0 20px; }
.sp-w b { font:600 16px var(--mono); color:var(--ink); overflow-wrap:anywhere; }
.sp-alsoline { padding:4px 24px 20px; display:flex; gap:12px; align-items:baseline; flex-wrap:wrap;
  border-top:1px dashed var(--line); margin:8px 24px 0; padding-left:0; padding-right:0; }
.sp-alsoline span { font:600 13px var(--mono); letter-spacing:1.4px; color:var(--slate6); }
.sp-alsoline b { font:600 16px var(--mono); color:var(--ink); overflow-wrap:anywhere; }

#sp-gate { margin-top:20px; width:100%; max-width:620px; display:flex; align-items:center; gap:16px;
  background:var(--page); border:2px solid var(--line); border-radius:12px; padding:18px 20px;
  cursor:pointer; text-align:left; transition:all .2s; }
#sp-gate.done { background:var(--greenlite); border-color:var(--greenbd); }
#sp-ck { width:28px; height:28px; flex:0 0 28px; border-radius:8px; border:2px solid var(--slate4);
  background:transparent; color:#fff; font:700 16px var(--sans); display:flex; align-items:center; justify-content:center; }
#sp-gate.done #sp-ck { background:var(--indigo); border-color:var(--indigo); }
#sp-gate .sp-gt { font:600 15px var(--sans); color:var(--ink); }
#sp-gate .sp-gh { font:400 13px var(--sans); color:var(--slate5); margin-top:4px; }

.sp-pwbox { margin-top:20px; border:1px solid var(--line); border-radius:12px; background:var(--panel);
  padding:20px 24px; max-width:620px; box-shadow:0 4px 6px -1px rgba(0,0,0,.05); }
.sp-pwbox .sp-lab2 { font:600 12px var(--mono); letter-spacing:1.6px; color:var(--indigo); }
#sp-pw-shown { font:600 22px var(--mono); color:var(--ink); margin-top:10px; word-break:break-all;
  background:var(--page); padding:12px 16px; border-radius:8px; border:1px solid var(--line2); }
.sp-pwafter { font:400 14px/1.6 var(--sans); color:var(--slate5); margin-top:16px; max-width:620px; }

#sp-locked-chip { font:600 11px var(--mono); letter-spacing:1.4px; color:var(--slate5); background:var(--line2);
  border:1px solid var(--line); border-radius:6px; padding:4px 10px; }
.sp-printrow { display:flex; align-items:center; gap:20px; margin-top:20px; flex-wrap:wrap; }
#sp-print { border:none; border-radius:10px; padding:16px 32px; font:600 16px var(--sans); cursor:pointer;
  background:var(--indigo); color:#fff; box-shadow:0 4px 12px rgba(0,0,0,.1); transition:all .2s; }
#sp-print:disabled { background:var(--line2); color:var(--slate4); cursor:default; box-shadow:none; }
.sp-printside { font:400 14px var(--sans); color:var(--slate5); }

/* ---- printed sheet ---- */
#sp-sheetwrap { margin-top:40px; display:none; }
#sp-legal { max-width:860px; margin:34px auto 0; padding:16px 20px; border-top:1px solid var(--line);
  font:400 12.5px/1.6 var(--sans); color:var(--slate5); text-align:center; }
.sp-sheet-legal { font:400 9px/1.4 var(--sans); color:var(--slate5); text-align:center;
  border-top:1px solid var(--line2); margin-top:10px; padding-top:8px; }
.sp-sheetlabel { font:600 12px var(--mono); letter-spacing:1.8px; color:var(--slate5); margin-bottom:14px; }
#sp-sheet { background:#fff; padding:36px; border:1px solid #E2E8F0; color:#0F172A;
  /* hardcoded light palette: the sheet must print black-on-white in any theme */
  --panel:#ffffff; --page:#F8FAFC; --ink:#0F172A; --slate7:#334155; --slate6:#475569;
  --slate5:#64748B; --slate4:#94A3B8; --line:#E2E8F0; --line2:#F1F5F9; --linemid:#CBD5E1;
  --green:#10B981; --greendark:#047857; --rose:#F43F5E; --rosedark:#BE123C;
  --rosepale:#FFF1F2; --reddark:#B91C1C;
  box-shadow:0 24px 48px -12px rgba(0,0,0,.15); display:flex; flex-direction:column; gap:16px; }
.sp-sheethead { display:flex; align-items:flex-end; justify-content:space-between; gap:24px; flex-wrap:wrap;
  border-bottom:3px solid var(--ink); padding-bottom:12px; }
.sp-sheettitle { font:700 22px var(--sans); letter-spacing:-.2px; color:var(--ink); }
.sp-btconly { font:700 11px var(--mono); letter-spacing:1.4px; color:#fff; background:var(--reddark);
  padding:4px 10px; border-radius:4px; margin-left:12px; vertical-align:2px; }
.sp-sheetnote { font:500 12px/1.5 var(--sans); color:var(--slate6); margin-top:6px; max-width:540px; }
.sp-sheetmeta { text-align:right; font:500 12px/1.5 var(--mono); color:var(--slate6); }

.sp-trow { border:2px solid var(--ink); display:flex; overflow:hidden; page-break-inside:avoid; }
.sp-tban { width:28px; flex:0 0 28px; display:flex; align-items:center; justify-content:center; }
.sp-tban span { -webkit-writing-mode:vertical-rl; writing-mode:vertical-rl; transform:rotate(180deg);
  font:700 11px var(--mono); letter-spacing:3px; color:#fff; }
.sp-tban.g { background:var(--green); }
.sp-tban.o { background:var(--rose); }
.sp-tban.k { background:var(--ink); }
.sp-tside { flex:1 1 0; min-width:0; padding:14px 16px; display:flex; gap:14px; align-items:center; }
.sp-tside.sec { background:var(--rosepale); }
.sp-tqr { width:104px; flex:0 0 104px; }
.sp-tqr canvas, .sp-tqr img { width:104px; height:104px; display:block; }
.sp-tinfo { min-width:0; flex:1; }
.sp-tinfo.r { text-align:right; }
.sp-tlab { font:700 12px var(--mono); letter-spacing:1.6px; }
.sp-tlab.g { color:var(--greendark); }
.sp-tlab.o { color:var(--rosedark); }
.sp-tsub { font:500 11px var(--sans); color:var(--slate6); margin-top:4px; }
.sp-tkey { font:600 12.5px/1.45 var(--mono); color:var(--ink); word-break:break-all; margin-top:10px; }
.sp-tmid { flex:0 0 120px; border-left:1px solid var(--linemid); border-right:1px solid var(--linemid);
  padding:14px 12px; display:flex; flex-direction:column; justify-content:space-between; text-align:center;
  background:var(--page); gap:6px; }
.sp-tnum { font:700 24px var(--mono); color:var(--ink); }
.sp-tpath { font:500 10px var(--mono); color:var(--slate5); margin-top:4px; word-break:break-all; }
.sp-tkeep { font:600 10px/1.3 var(--sans); color:var(--slate6); }
.sp-tamount { text-align:left; }
.sp-tamount div:first-child { font:700 10px var(--mono); letter-spacing:1.2px; color:var(--slate5); }
.sp-tamount .sp-line2x { border-bottom:1px solid var(--slate4); height:16px; }
@media (max-width:700px){ .sp-tmid { display:none; } }

.sp-guide { border:2px solid var(--ink); display:flex; page-break-inside:avoid; }
.sp-guidebody { flex:1; padding:16px 20px; display:grid; grid-template-columns:1fr 1fr; gap:12px 32px; }
@media (max-width:640px){ .sp-guidebody { grid-template-columns:1fr; } }
.sp-ghead { grid-column:1 / -1; font:700 12px var(--mono); letter-spacing:1.8px; color:var(--slate7);
  border-bottom:2px solid var(--line); padding-bottom:8px; }
.sp-gitem { font:500 12px/1.55 var(--sans); color:var(--ink); }
.sp-gitem b { font-weight:700; }
.sp-gfoot { grid-column:1 / -1; font:500 11.5px/1.5 var(--sans); color:var(--slate6);
  border-top:1px solid var(--line); padding-top:10px; }

@media print {
  body.simple-printing #simple-panel > *:not(#sp-sheetwrap) { display:none !important; }
  body.simple-printing .sp-sheetlabel { display:none !important; }
  body.simple-printing #advanced-wrap { display:none !important; }
  body.simple-printing { background:#fff; }
  body.simple-printing #sp-sheetwrap { margin:0; }
  #sp-sheet { box-shadow:none; padding:0; border:none; }
  .sp-tban.g { background:var(--green) !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .sp-tban.o { background:var(--rose) !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .sp-tban.k { background:var(--ink) !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .sp-btconly { background:var(--reddark) !important; color:#fff !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
}
</style>
<div id="simple-panel">
  <div class="sp-app">
    <div class="sp-apphead">
      <div><span class="sp-appname">BSV Paper Wallet</span><span class="sp-appver">iancoleman/bip39 v0.5.6 &middot; offline generator</span></div>
      <div style="display:flex; align-items:center; gap:10px"><button type="button" id="sp-theme-btn" title="Light / dark">&#127769;</button><div class="sp-pill off" id="sp-net-pill"><span class="sp-dot"></span><span id="sp-net-txt">OFFLINE &middot; SAFE</span></div></div>
    </div>
    <div id="sp-net-banner" style="display:none">
      <div class="sp-bang">!</div>
      <div><b>This computer is connected to the internet.</b> Generating here is fine to look around, but
        never for a wallet that will hold money. Turn off Wi-Fi (and unplug the internet cable if this
        computer uses one): the badge above will turn green by itself.</div>
    </div>
    <div id="sp-handheld-banner">
      <div class="sp-bang">!</div>
      <div><b>This is a phone or tablet.</b> Everything works here. A phone cannot be started from a
        live USB, so it cannot reach the cleanest setup: treat it as you would your everyday computer,
        not as a dedicated offline machine. Write the seed phrase down by hand as asked below and
        <b>never take a screenshot of it</b>, since phone screenshots usually sync to the cloud. Printing
        is easier from a computer, on a printer connected by cable.</div>
    </div>
    <div class="sp-body">
      <div class="sp-hero">Bitcoin SV ($BSV) wallets, printed on paper.</div>
      <div class="sp-herosub">One seed phrase you write by hand backs up every wallet you print.</div>

      <div id="sp-dirty">
        <div class="sp-bang2">!</div>
        <div><b>Settings changed since you generated.</b> The sheet below no longer matches your choices.
          Press <b>Generate again</b> before printing.</div>
      </div>

      <div class="sp-setup">
        <div class="sp-setup-grid">
          <div class="sp-cell sp-cell-r">
            <div class="sp-lab">SEED PHRASE LENGTH</div>
            <div class="sp-choices">
              <button type="button" class="sp-choice" id="sp-w12"><b>12 words</b><span>Faster to write</span></button>
              <button type="button" class="sp-choice sel" id="sp-w24"><b>24 words</b><span>Recommended</span></button>
            </div>
          </div>
          <div class="sp-cell">
            <div class="sp-lab">HOW MANY PAPER WALLETS</div>
            <div class="sp-counter">
              <div class="sp-counterbox">
                <button type="button" id="sp-dec">&#8722;</button>
                <div id="sp-count-display">3</div>
                <button type="button" id="sp-inc">+</button>
              </div>
              <div class="sp-counter-note">Separate addresses, one per wallet. Same seed.</div>
            </div>
          </div>
        </div>
        <div class="sp-pwrow">
          <button type="button" class="sp-switch" id="sp-pw-switch"><span class="sp-knob"></span></button>
          <div class="sp-pwmain">
            <div class="sp-pwtitle"><b>Optional:</b> lock the printed keys with a password
              <span class="sp-chip">BIP38</span></div>
            <div class="sp-pwstate" id="sp-pw-stateline">Off: the private keys are printed as plain text,
              so keep the paper hidden. Turn this on only if you want the keys encrypted too, in case
              someone finds the printout.</div>
            <div id="sp-pw-wrap">
              <div class="sp-pwline">
                <input id="sp-bip38-pw" type="password" autocomplete="off" maxlength="64"
                  placeholder="e.g. paper-otter-lantern-42">
                <button type="button" id="sp-pw-show">Show</button>
              </div>
              <input id="sp-bip38-pw2" type="password" autocomplete="off" maxlength="64"
                placeholder="Re-type the password to confirm">
              <div id="sp-pw-mismatch">Passwords don&#39;t match yet.</div>
              <div class="sp-pwnote">Use several words: a single one can be guessed by a program. Spaces or
                dashes work equally well.</div>
            </div>
          </div>
        </div>
        <div class="sp-setup-foot">
          <div><div id="sp-summary">3 wallets from one 24-word seed phrase.</div>
            <div id="sp-regen-note">Generating again replaces the current result.</div></div>
          <button type="button" id="sp-generate">Generate</button>
        </div>
      </div>
      <div id="simple-status"></div>

      <div id="sp-genbox">
        <div class="sp-genhead"><span class="sp-spin"></span><span id="sp-gen-label">Generating…</span></div>
        <div class="sp-gensub">This can take a moment.</div>
      </div>

      <div id="sp-steps">
        <div class="sp-st">
          <div class="sp-strail"><div class="sp-snum">1</div><div class="sp-line"></div></div>
          <div class="sp-sbody">
            <div class="sp-stitle">Write down your seed phrase</div>
            <div class="sp-ssub">These words are never printed and never leave this screen: printers keep
              copies of what they print. Write them in order, on paper, with the last line included.
              For long-term storage, a stamped steel seed plate survives fire and water better than
              paper.</div>
            <div id="sp-warn-onscreen">
              <div class="sp-bang3">!</div>
              <div><b>The words are visible.</b> Take your time to write them down, then press Hide when you
        are done. Nobody else, and no camera, should see the screen while they show.</div>
            </div>
            <div class="sp-secretbox">
              <div class="sp-secrethead">
                <span id="sp-seedcount">SECRET &middot; 24 WORDS</span>
                <button type="button" id="sp-seed-btn">Reveal seed phrase</button>
              </div>
              <div id="sp-seed-hiddenmsg">Hidden. Reveal them when you are alone and no camera is
                pointing at the screen.</div>
              <div id="sp-seed-open" style="display:none">
                <div id="sp-seed-grid"></div>
                <div class="sp-alsoline"><span>ALSO WRITE THIS LINE</span><b id="sp-path-inline"></b></div>
              </div>
            </div>
            <button type="button" id="sp-gate">
              <div id="sp-ck"></div>
              <div><div class="sp-gt" id="sp-gate-title">I have written all 24 words on paper and checked
                them twice</div>
              <div class="sp-gh" id="sp-gate-hint">Tick this to unlock printing.</div></div>
            </button>
          </div>
        </div>

        <div class="sp-st">
          <div class="sp-strail"><div class="sp-snum idle" id="sp-n2">2</div><div class="sp-line"></div></div>
          <div class="sp-sbody sp-dim" id="sp-body-pw">
            <div id="sp-pw-step-on" style="display:none">
              <div class="sp-stitle">Save your password</div>
              <div class="sp-ssub">It is never printed. You will be asked for it every time you spend from
                these wallets, typed exactly as it is here: capitals, spaces and dashes all count.</div>
              <div class="sp-pwbox">
                <div class="sp-lab2">YOUR PASSWORD</div>
                <div id="sp-pw-shown"></div>
              </div>
              <div class="sp-pwafter">Memorize it, or write it on a separate sheet kept away from the
                printed wallets. Lose it and those printed keys are gone, but your handwritten seed phrase
                still restores every wallet, because the password protects only the printed keys.</div>
            </div>
            <div id="sp-pw-step-off">
              <div class="sp-stitle gray">Save your password</div>
              <div class="sp-ssub gray">Password protection is off, so there is nothing to save here. If you
                want the printed keys encrypted too, switch on <b>&quot;Lock the printed keys&quot;</b> in
                the setup above and generate again.</div>
            </div>
          </div>
        </div>

        <div class="sp-st">
          <div class="sp-strail"><div class="sp-snum idle" id="sp-n-print">3</div><div class="sp-line"></div></div>
          <div class="sp-sbody sp-dim" id="sp-body-print">
            <div class="sp-stitle">Print the wallets <span id="sp-locked-chip">&#128274; LOCKED &middot;
              TICK THE BOX IN STEP 1</span></div>
            <div class="sp-ssub" id="sp-print-sub">Unlocks once you confirm the seed phrase is written down.
              That handwritten copy is the only thing that survives a lost or ruined printout.</div>
            <div class="sp-printrow">
              <button type="button" id="sp-print" disabled>Print 3 paper wallets</button>
              <div class="sp-printside">A printer connected by USB cable is safest. No printer? Save as
                PDF works too, but keep that file only on a computer that stays offline: it contains the
                private keys.</div>
            </div>
          </div>
        </div>

        <div class="sp-st">
          <div class="sp-strail"><div class="sp-snum idle" id="sp-n-check">4</div></div>
          <div class="sp-sbody sp-dim" id="sp-body-check">
            <div class="sp-stitle">Check the print before you send money</div>
            <div class="sp-ssub">Scan each green DEPOSIT code with your phone: it must show exactly the
              address printed beneath it. Green is public and always safe to scan. Never scan a SECRET
              code until the day you spend that wallet.</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div id="sp-legal">
    Free and open-source software, provided as is and with no warranty of any kind. You alone hold
    these keys: nobody can recover them for you, and no loss can be reversed. Test the whole process
    with a small amount before trusting it with more.
  </div>

  <div id="sp-sheetwrap">
    <div class="sp-sheetlabel">WHAT COMES OUT OF THE PRINTER</div>
    <div id="sp-sheet">
      <div class="sp-sheethead">
        <div>
          <div class="sp-sheettitle">Bitcoin SV ($BSV) Paper Wallets<span class="sp-btconly">$BSV ONLY
            &middot; NOT $BTC</span></div>
          <div class="sp-sheetnote">Keep this sheet whole and store it somewhere safe: that is enough. If
            you prefer, cut it into strips along the gaps, one wallet per strip, the two halves of each
            wallet always staying together.</div>
        </div>
        <div class="sp-sheetmeta" id="sp-sheet-meta"></div>
      </div>
      <div id="sp-addr-list"></div>
      <div class="sp-guide">
        <div class="sp-tban k"><span>GUIDE</span></div>
        <div class="sp-guidebody">
          <div class="sp-ghead">HOW TO USE THESE PAPER WALLETS</div>
          <div class="sp-gitem"><b>1 &middot; Check.</b> Scan each green code and confirm it matches the
            address printed beside it.</div>
          <div class="sp-gitem"><b>2 &middot; Load.</b> Send BSV to the green deposit address. Fill wallet
            #0 first, then #1, in order.</div>
          <div class="sp-gitem"><b>3 &middot; Spend.</b> Sweep the wallet in an app that imports private
            keys, moving the whole balance in one go. ElectrumSVP does this, including keys that start
            with 6P: it asks for your password and decrypts them for you.</div>
          <div class="sp-gitem"><b>4 &middot; Rule.</b> Never photograph or scan a SECRET code until the
            day you spend that wallet.</div>
          <div class="sp-gfoot">Lost or damaged wallets: restore everything from your handwritten seed
            phrase using the derivation path <b>m/44'/236'/0'</b>, in ElectrumSVP (electrumsv.io) or any
            other BIP39 wallet that lets you set that path.</div>
          <div class="sp-gfoot sp-sheet-legal">Made with the open-source BSV Paper Wallet generator,
            provided as is and with no warranty. You alone are responsible for these keys.</div>
        </div>
      </div>
    </div>
  </div>
</div>
<script id="simple-mode-script">
(function(){
  "use strict";
  var statusEl = null;
  var pollTimer = null, lastAddr = null, stable = 0;
  var wantCount = 3, wantWords = 24, wantBip38 = false, lastPw = "", written = false;
  var doneShown = false, revealTimer = null, revealLeft = 0;
  var BSVLOGO = "__BSVLOGO__";
  var bsvImg = new Image();
  bsvImg.src = BSVLOGO;

  function setStatus(t){ statusEl.textContent = t; }

  function qr(el, text, logo){
    el.innerHTML = "";
    var opts = { text:text, render:"canvas", size:360, ecLevel:(logo ? "H" : "M"), quiet:2 };
    if (logo && bsvImg.complete && bsvImg.naturalWidth > 0) {
      opts.mode = "image"; opts.image = bsvImg; opts.mSize = 20;
    }
    var c = libs.kjua(opts);
    c.style.width = "104px";
    c.style.height = "104px";
    el.appendChild(c);
  }

  function readRows(n){
    var trs = document.querySelectorAll(".addresses tr");
    if (trs.length < n) return null;
    var out = [];
    for (var i = 0; i < n; i++) {
      var row = trs[i];
      var g = function(sel){ var el = row.querySelector(sel); return el ? el.textContent.replace(/\s+/g,"") : ""; };
      var r = { path:g(".index span"), addr:g(".address span"), wif:g(".privkey span") };
      if (!(r.addr && r.addr.charAt(0) === "1" && r.wif && r.path)) return null;
      if (wantBip38 && r.wif.indexOf("6P") !== 0) return null;
      if (!wantBip38 && r.wif.indexOf("6P") === 0) return null;
      out.push(r);
    }
    return out;
  }

  function bsvSelected(){
    var sel = document.querySelector(".network");
    var opt = sel && sel.options[sel.selectedIndex];
    return !!(opt && opt.textContent.indexOf("BSV") !== -1);
  }

  function updateSummary(){
    document.getElementById("sp-count-display").textContent = wantCount;
    document.getElementById("sp-dec").disabled = wantCount <= 1;
    document.getElementById("sp-inc").disabled = wantCount >= 20;
    document.getElementById("sp-summary").textContent = wantCount + " wallet" + (wantCount > 1 ? "s" : "") +
      " from one " + wantWords + "-word seed phrase" +
      (wantBip38 ? ", printed keys locked with a password." : ".");
    document.getElementById("sp-print").textContent =
      "Print " + wantCount + " paper wallet" + (wantCount > 1 ? "s" : "");
  }

  function markDirty(){
    if (doneShown) { document.getElementById("sp-dirty").style.display = "flex"; }
  }

  function applyGate(){
    var gate = document.getElementById("sp-gate");
    gate.className = written ? "done" : "";
    document.getElementById("sp-ck").textContent = written ? "✓" : "";
    document.getElementById("sp-gate-hint").textContent = written ? "Printing unlocked." : "Tick this to unlock printing.";
    document.getElementById("sp-locked-chip").style.display = written ? "none" : "inline-block";
    document.getElementById("sp-print").disabled = !written;
    document.getElementById("sp-print-sub").textContent = written
      ? "Ready. The sheet below is exactly what will come out of the printer."
      : "Unlocks once you confirm the seed phrase is written down. That handwritten copy is the only thing that survives a lost or ruined printout.";
    document.getElementById("sp-n-print").className = written ? "sp-snum" : "sp-snum idle";
    document.getElementById("sp-n-check").className = written ? "sp-snum" : "sp-snum idle";
    document.getElementById("sp-body-print").className = written ? "sp-sbody" : "sp-sbody sp-dim";
    document.getElementById("sp-body-check").className = written ? "sp-sbody" : "sp-sbody sp-dim";
  }

  function stopReveal(){
    if (revealTimer) { clearInterval(revealTimer); revealTimer = null; }
    revealLeft = 0;
  }

  function hideSeed(){
    stopReveal();
    document.getElementById("sp-seed-open").style.display = "none";
    document.getElementById("sp-seed-hiddenmsg").style.display = "block";
    document.getElementById("sp-warn-onscreen").style.display = "none";
    document.getElementById("sp-seed-btn").textContent = "Reveal seed phrase";
  }

  function render(phrase, rows){
    document.getElementById("sp-genbox").style.display = "none";
    var grid = document.getElementById("sp-seed-grid");
    grid.innerHTML = "";
    var words = phrase.split(/\s+/);
    for (var j = 0; j < words.length; j++) {
      var w = document.createElement("div");
      w.className = "sp-w";
      var num = document.createElement("i"); num.textContent = j + 1;
      var txt = document.createElement("b"); txt.textContent = words[j];
      w.appendChild(num); w.appendChild(txt);
      grid.appendChild(w);
    }
    var acct = rows[0].path.replace(/\/0\/\d+$/, "");
    document.getElementById("sp-path-inline").textContent = "BSV · BIP39 · " + acct;
    document.getElementById("sp-seedcount").textContent = "SECRET · " + words.length + " WORDS";
    document.getElementById("sp-gate-title").textContent =
      "I have written all " + words.length + " words on paper and checked them twice";

    hideSeed();
    written = false;
    applyGate();

    // password step (always visible; on/off variants)
    document.getElementById("sp-pw-step-on").style.display = wantBip38 ? "block" : "none";
    document.getElementById("sp-pw-step-off").style.display = wantBip38 ? "none" : "block";
    document.getElementById("sp-n2").className = wantBip38 ? "sp-snum" : "sp-snum idle";
    document.getElementById("sp-body-pw").className = wantBip38 ? "sp-sbody" : "sp-sbody sp-dim";
    document.getElementById("sp-pw-shown").textContent = wantBip38 ? lastPw : "";

    // sheet
    document.getElementById("sp-sheet-meta").innerHTML =
      "BIP39 · " + acct + "<br>" + words.length + "-word seed" +
      (wantBip38 ? " · password-protected" : "");
    var list = document.getElementById("sp-addr-list");
    list.innerHTML = "";
    for (var i = 0; i < rows.length; i++) {
      var r = rows[i];
      var row = document.createElement("div");
      row.className = "sp-trow";
      row.style.marginBottom = "16px";
      row.innerHTML =
        '<div class="sp-tban g"><span>SHARE</span></div>' +
        '<div class="sp-tside">' +
          '<div class="sp-tqr"></div>' +
          '<div class="sp-tinfo">' +
            '<div class="sp-tlab g">DEPOSIT ADDRESS</div>' +
            '<div class="sp-tsub">Public, safe to scan and share. Send <b>$BSV only</b>.</div>' +
            '<div class="sp-tkey"></div>' +
          '</div>' +
        '</div>' +
        '<div class="sp-tmid">' +
          '<div><div class="sp-tnum">#' + i + '</div><div class="sp-tpath">' + r.path + '</div></div>' +
          '<div class="sp-tkeep">Keep both halves together</div>' +
          '<div class="sp-tamount"><div>AMOUNT / NOTES</div><div class="sp-line2x"></div><div class="sp-line2x"></div></div>' +
        '</div>' +
        '<div class="sp-tside sec">' +
          '<div class="sp-tinfo r">' +
            '<div class="sp-tlab o">' + (wantBip38 ? 'PRIVATE KEY · LOCKED' : 'PRIVATE KEY') + '</div>' +
            '<div class="sp-tsub">' + (wantBip38 ? 'Needs your password to spend. Keep secret.' : 'Anyone holding this can spend. Keep secret.') + '</div>' +
            '<div class="sp-tkey"></div>' +
          '</div>' +
          '<div class="sp-tqr"></div>' +
        '</div>' +
        '<div class="sp-tban o"><span>SECRET</span></div>';
      var keys = row.querySelectorAll(".sp-tkey");
      keys[0].textContent = r.addr;
      keys[1].textContent = r.wif;
      var qrs = row.querySelectorAll(".sp-tqr");
      qr(qrs[0], r.addr, true);
      qr(qrs[1], r.wif);
      list.appendChild(row);
    }

    doneShown = true;
    document.getElementById("sp-dirty").style.display = "none";
    document.getElementById("sp-steps").style.display = "block";
    document.getElementById("sp-sheetwrap").style.display = "block";
    document.getElementById("sp-generate").textContent = "Generate again";
    document.getElementById("sp-regen-note").style.display = "block";
    setStatus("Done: " + rows.length + " paper wallet" + (rows.length > 1 ? "s" : "") +
      " from one " + words.length + "-word seed phrase" +
      (wantBip38 ? ", private keys password-protected" : "") + ". Follow the steps below.");
  }

  function poll(){
    var phraseNode = document.querySelector(".phrase");
    var phrase = phraseNode ? phraseNode.value.trim() : "";
    var rows = readRows(wantCount);
    var ok = !!(rows && phrase.split(/\s+/).length === wantWords && bsvSelected());
    if (ok && rows[rows.length-1].addr === lastAddr) { stable++; } else { stable = 0; }
    lastAddr = ok ? rows[rows.length-1].addr : null;
    if (ok && stable >= 2) {
      clearInterval(pollTimer); pollTimer = null;
      render(phrase, rows);
    }
  }

  function generateClickedSimple(){
    if (pollTimer) { clearInterval(pollTimer); pollTimer = null; }
    var pwInput = document.getElementById("sp-bip38-pw");
    var pwConfirm = document.getElementById("sp-bip38-pw2");
    var bip38pw = wantBip38 ? pwInput.value : "";
    if (wantBip38 && bip38pw.length === 0) {
      setStatus("Type a password first, or switch the password lock off.");
      return;
    }
    if (wantBip38 && bip38pw !== pwConfirm.value) {
      setStatus("The two password fields do not match yet.");
      document.getElementById("sp-pw-mismatch").style.display = "block";
      return;
    }
    lastPw = bip38pw;
    document.getElementById("sp-steps").style.display = "none";
    document.getElementById("sp-sheetwrap").style.display = "none";
    document.getElementById("sp-dirty").style.display = "none";
    document.getElementById("sp-gen-label").textContent = "Generating " + wantCount +
      " wallet" + (wantCount > 1 ? "s" : "") + (wantBip38 ? " (password encryption is slow on purpose)" : "") + "…";
    document.getElementById("sp-genbox").style.display = "block";
    setStatus("");
    try {
      $("#strength").val(String(wantWords));
      $(".use-entropy").prop("checked", false).trigger("change");
      $(".passphrase").val("").trigger("input");
      $(".use-bip38").prop("checked", wantBip38);
      $(".bip38-password").val(wantBip38 ? bip38pw : "");
      // only derive as many rows as requested (matters a lot with BIP38: each key costs seconds)
      $(".rows-to-add").val(String(wantCount));
      var bsvVal = null;
      $(".network option").each(function(){
        if ($(this).text().indexOf("BSV") !== -1) { bsvVal = $(this).val(); }
      });
      if (bsvVal === null) { setStatus("ERROR: BSV not found in coin list."); document.getElementById("sp-genbox").style.display = "none"; return; }
      $(".network").val(bsvVal).trigger("change");
      setTimeout(function(){
        // upstream generateClicked() ignores the click unless the button has focus
        var g = $(".generate");
        try { g[0].focus({ preventScroll: true }); } catch(err) { g[0].focus(); }
        g.trigger("click");
        lastAddr = null; stable = 0;
        pollTimer = setInterval(poll, 350);
      }, 600);
    } catch(e) {
      setStatus("ERROR: " + e.message);
      document.getElementById("sp-genbox").style.display = "none";
    }
  }

  function clearStaleFeedback(){
    var phraseNode = document.querySelector(".phrase");
    if (!phraseNode || !phraseNode.value.trim()) {
      var fb = document.querySelector(".feedback");
      if (fb) { fb.textContent = ""; }
    }
  }

  function setWords(n){
    if (wantWords !== n) { markDirty(); }
    wantWords = n;
    document.getElementById("sp-w12").className = n === 12 ? "sp-choice sel" : "sp-choice";
    document.getElementById("sp-w24").className = n === 24 ? "sp-choice sel" : "sp-choice";
    updateSummary();
  }

  function isHandheld(){
    // primary pointer coarse = finger, and a screen too small to be a touch laptop
    return window.matchMedia("(pointer: coarse)").matches &&
           window.matchMedia("(max-width: 1024px)").matches;
  }

  function updateNet(){
    var online = navigator.onLine;
    var pill = document.getElementById("sp-net-pill");
    var txt = document.getElementById("sp-net-txt");
    var netBanner = document.getElementById("sp-net-banner");
    var handBanner = document.getElementById("sp-handheld-banner");
    if (isHandheld()) {
      // connectivity is not the deciding factor on a phone, so never show the green SAFE state
      pill.className = "sp-pill warn";
      txt.textContent = "PHONE · EXPLORE ONLY";
      handBanner.style.display = "flex";
      netBanner.style.display = "none";
      return;
    }
    handBanner.style.display = "none";
    pill.className = online ? "sp-pill on" : "sp-pill off";
    txt.textContent = online ? "ONLINE · NOT SAFE" : "OFFLINE · SAFE";
    netBanner.style.display = online ? "flex" : "none";
  }

  function cleanupAdvanced(){
    var bsvVal = null;
    $(".network option").each(function(){
      if ($(this).text().indexOf("BSV") !== -1) { bsvVal = $(this).val(); }
    });
    if (bsvVal !== null) { $(".network").val(bsvVal).trigger("change"); }
    var s = document.getElementById("strength");
    if (s) {
      for (var i = s.options.length - 1; i >= 0; i--) {
        var v = s.options[i].value;
        if (v !== "12" && v !== "24") { s.remove(i); }
      }
      s.value = "24";
    }
  }

  function boot(){
    var panel = document.getElementById("simple-panel");
    var wrap = document.createElement("div");
    wrap.id = "advanced-wrap";
    wrap.className = "sp-collapsed";
    var keep = { "simple-panel":1, "simple-mode-style":1, "simple-mode-script":1, "advanced-wrap":1 };
    var nodes = [];
    for (var i = 0; i < document.body.children.length; i++) {
      var el = document.body.children[i];
      if (!keep[el.id]) { nodes.push(el); }
    }
    for (var j = 0; j < nodes.length; j++) { wrap.appendChild(nodes[j]); }
    document.body.insertBefore(panel, document.body.firstChild);
    document.body.appendChild(wrap);

    statusEl = document.getElementById("simple-status");
    document.title = "BSV Paper Wallet"; // also names the saved PDF
    document.body.classList.add("sp-ready");

    document.getElementById("sp-generate").addEventListener("click", generateClickedSimple);
    document.getElementById("sp-w12").addEventListener("click", function(){ setWords(12); });
    document.getElementById("sp-w24").addEventListener("click", function(){ setWords(24); });
    document.getElementById("sp-inc").addEventListener("click", function(){
      if (wantCount < 20) { wantCount++; markDirty(); } updateSummary();
    });
    document.getElementById("sp-dec").addEventListener("click", function(){
      if (wantCount > 1) { wantCount--; markDirty(); } updateSummary();
    });
    document.getElementById("sp-pw-switch").addEventListener("click", function(){
      wantBip38 = !wantBip38;
      markDirty();
      this.className = wantBip38 ? "sp-switch on" : "sp-switch";
      document.getElementById("sp-pw-wrap").style.display = wantBip38 ? "flex" : "none";
      document.getElementById("sp-pw-stateline").textContent = wantBip38
        ? "On: the private keys are printed encrypted, so nobody can spend them without this password. Generating is slower: up to a minute per wallet."
        : "Off: the private keys are printed as plain text, so keep the paper hidden. Turn this on only if you want the keys encrypted too, in case someone finds the printout.";
      if (!wantBip38) {
        document.getElementById("sp-bip38-pw").value = "";
        document.getElementById("sp-bip38-pw2").value = "";
        document.getElementById("sp-pw-mismatch").style.display = "none";
        document.getElementById("sp-bip38-pw2").className = "";
      } else {
        document.getElementById("sp-bip38-pw").focus();
      }
      updateSummary();
    });
    document.getElementById("sp-pw-show").addEventListener("click", function(){
      var a = document.getElementById("sp-bip38-pw");
      var b = document.getElementById("sp-bip38-pw2");
      var showing = a.type === "text";
      a.type = showing ? "password" : "text";
      b.type = showing ? "password" : "text";
      this.textContent = showing ? "Show" : "Hide";
    });
    function checkMatch(){
      var a = document.getElementById("sp-bip38-pw").value;
      var b = document.getElementById("sp-bip38-pw2");
      var bad = b.value.length > 0 && a !== b.value;
      document.getElementById("sp-pw-mismatch").style.display = bad ? "block" : "none";
      b.className = bad ? "bad" : "";
    }
    document.getElementById("sp-bip38-pw").addEventListener("input", checkMatch);
    document.getElementById("sp-bip38-pw2").addEventListener("input", checkMatch);

    document.getElementById("sp-seed-btn").addEventListener("click", function(){
      var open = document.getElementById("sp-seed-open");
      var btn = this;
      if (open.style.display !== "none") { hideSeed(); return; }
      if (revealTimer) { stopReveal(); btn.textContent = "Reveal seed phrase"; return; }
      revealLeft = 3;
      btn.textContent = "Revealing in 3…";
      revealTimer = setInterval(function(){
        revealLeft--;
        if (revealLeft > 0) {
          btn.textContent = "Revealing in " + revealLeft + "…";
        } else {
          stopReveal();
          open.style.display = "block";
          document.getElementById("sp-seed-hiddenmsg").style.display = "none";
          document.getElementById("sp-warn-onscreen").style.display = "flex";
          btn.textContent = "Hide";
        }
      }, 700);
    });
    document.getElementById("sp-gate").addEventListener("click", function(){
      written = !written;
      applyGate();
    });
    document.getElementById("sp-print").addEventListener("click", function(){
      if (!written) { return; }
      document.body.classList.add("simple-printing");
      window.print();
      setTimeout(function(){ document.body.classList.remove("simple-printing"); }, 500);
    });
    window.addEventListener("afterprint", function(){
      document.body.classList.remove("simple-printing");
    });

    var themeBtn = document.getElementById("sp-theme-btn");
    function darkActive(){
      var r = document.documentElement;
      if (r.className.indexOf("sp-dark") !== -1) return true;
      if (r.className.indexOf("sp-light") !== -1) return false;
      return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    }
    function themeIcon(){ themeBtn.innerHTML = darkActive() ? "&#9728;&#65039;" : "&#127769;"; }
    themeBtn.addEventListener("click", function(){
      var r = document.documentElement;
      var toDark = !darkActive();
      r.classList.remove("sp-dark", "sp-light");
      r.classList.add(toDark ? "sp-dark" : "sp-light");
      themeIcon();
    });
    themeIcon();

    window.addEventListener("online", updateNet);
    window.addEventListener("offline", updateNet);
    window.addEventListener("resize", updateNet);
    window.addEventListener("orientationchange", updateNet);
    updateNet();
    updateSummary();

    try { cleanupAdvanced(); } catch(e) { /* engine stays as-is on failure */ }
    setTimeout(clearStaleFeedback, 700); // after the boot-time network switch settles
  }
  if (document.readyState === "complete") { setTimeout(boot, 400); }
  else { window.addEventListener("load", function(){ setTimeout(boot, 400); }); }
  // last resort: never leave the visitor staring at a loading screen with no explanation
  setTimeout(function(){
    if (!document.body.classList.contains("sp-ready")) {
      document.body.classList.add("sp-stalled");
    }
  }, 15000);
})();
</script>
'''

src = io.open(SRC, encoding='utf-8').read()
assert src.count('</body>') == 1, 'unexpected file structure'

# Pre-boot style injected right after <body>: hides the upstream UI while the big
# file parses (prevents the flash of the raw Coleman page) and shows a loading
# hint. simple-mode-style at the end of the body re-enables our own sections.
i = src.find('<body')
assert i != -1, 'no body tag'
j = src.find('>', i)
preboot = (
    '<style id="sp-preboot">'
    'body>*{display:none !important}'
    'body>noscript{display:block !important}'
    'body::before{content:"Loading BSV Paper Wallet\2026";position:fixed;top:38%;left:0;right:0;'
    'text-align:center;font:16px sans-serif;color:#555}'
    # if the script runs but never finishes booting, say something instead of spinning forever
    'body.sp-stalled::before{content:"This is taking too long. Open the file directly in Chrome, '
    'Firefox, Safari or Edge: some viewer apps block scripts.";padding:0 24px;line-height:1.5;color:#8a5a00}'
    '</style>'
    # scripting disabled entirely: the loading text would never clear, so replace it
    '<noscript>'
    '<style>body::before{content:none !important}</style>'
    '<div style="max-width:620px;margin:14vh auto;padding:22px;border:1px solid #e0c48a;'
    'background:#fffbeb;border-radius:12px;font:15px/1.6 system-ui,sans-serif;color:#7a4c00">'
    '<b>JavaScript is switched off, so this generator cannot run.</b> It creates your keys inside the '
    'browser itself, which is exactly why nothing is ever sent anywhere, and that needs scripting.'
    '<br><br>Open this file directly in Chrome, Firefox, Safari or Edge. Some &quot;HTML viewer&quot; '
    'apps block scripts. Note that this generator is meant for a computer: a phone cannot be taken '
    'properly offline.'
    '</div></noscript>')
src = src[:j+1] + preboot + src[j+1:]

logo_uri = io.open('assets/bsv-logo-datauri.txt', encoding='utf-8').read().strip()
patch = patch.replace('__BSVLOGO__', logo_uri)
out = src.replace('</body>', patch + '\n</body>')
io.open(OUT, 'w', encoding='utf-8').write(out)
print('written', OUT, len(out))
