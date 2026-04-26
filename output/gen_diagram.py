import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(20, 24))
ax.set_xlim(0, 20)
ax.set_ylim(0, 24)
ax.axis('off')
fig.patch.set_facecolor('white')

AW, AH = 5.8, 1.8
LW, LH = 5.2, 1.8

IX,  IY  = 10.0, 23.2
ACX, ACY = 10.0, 20.0
AUX, AUY = 10.0, 13.5
LKX, LKY =  2.9, 13.5
FX,  FY  =  10.0,  4.5

def sbox(cx, cy, w, h, name, sub=None, fc='#dce8f5'):
    p = FancyBboxPatch((cx-w/2, cy-h/2), w, h,
                       boxstyle="round,pad=0.15", lw=2.0,
                       edgecolor='#222', facecolor=fc, zorder=3)
    ax.add_patch(p)
    if sub:
        ax.plot([cx-w/2+0.15, cx+w/2-0.15], [cy+0.1, cy+0.1],
                color='#777', lw=0.9, zorder=4)
        ax.text(cx, cy+0.5,  name, ha='center', va='center',
                fontsize=13, fontweight='bold', zorder=5)
        ax.text(cx, cy-0.38, sub, ha='center', va='center',
                fontsize=9.5, style='italic', color='#333', zorder=5)
    else:
        ax.text(cx, cy, name, ha='center', va='center',
                fontsize=13, fontweight='bold', zorder=5)

def init_ps(cx, cy):
    ax.add_patch(plt.Circle((cx, cy), 0.28, color='black', zorder=6))

def final_ps(cx, cy):
    ax.add_patch(plt.Circle((cx, cy), 0.36, color='black',  zorder=6))
    ax.add_patch(plt.Circle((cx, cy), 0.24, color='white',  zorder=7))
    ax.add_patch(plt.Circle((cx, cy), 0.14, color='black',  zorder=8))

def arr(x1, y1, x2, y2, lbl='', rad=0.0,
        lx=None, ly=None, fs=8.5, fc='white', zorder=4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#111', lw=1.6,
                                connectionstyle=f'arc3,rad={rad}'),
                zorder=zorder)
    if lbl:
        mx = (x1+x2)/2 if lx is None else lx
        my = (y1+y2)/2 if ly is None else ly
        ax.text(mx, my, lbl, ha='center', va='center', fontsize=fs,
                color='#111', zorder=zorder+1,
                bbox=dict(boxstyle='round,pad=0.25', fc=fc, ec='#999',
                          alpha=0.96, lw=0.8))

def self_loop(cx, cy, side, lbl, lx, ly, yoff=0.5, fs=8.2):
    sign = 1 if side == 'right' else -1
    xe = cx + sign * AW/2
    ax.annotate('', xy=(xe, cy-yoff), xytext=(xe, cy+yoff),
                arrowprops=dict(arrowstyle='->', color='#111', lw=1.6,
                                connectionstyle=f'arc3,rad={sign*0.85}'),
                zorder=4)
    ax.text(lx, ly, lbl, ha='center', va='center', fontsize=fs,
            color='#111', zorder=5,
            bbox=dict(boxstyle='round,pad=0.25', fc='#fffbe6',
                      ec='#c0a000', alpha=0.96, lw=1.0))

# ── states ────────────────────────────────────────────────────────────────────
sbox(ACX, ACY, AW, AH, 'Active',
     sub='entry / authTime := -1', fc='#dce8f5')
sbox(AUX, AUY, AW, AH, 'Authenticated',
     sub='entry / authTime := time()', fc='#d5f0d5')
sbox(LKX, LKY, LW, LH, 'Locked', fc='#f5e0dc')
init_ps(IX, IY)
final_ps(FX, FY)

# ── T1: Initial → Active ──────────────────────────────────────────────────────
arr(IX, IY-0.28, ACX, ACY+AH/2,
    lbl='Session(account, webInterface) /\nuser:=account; ui:=webInterface; authTime:=-1',
    lx=15.5, ly=22.0, fs=8.8, fc='#f2f2f2')

# ── T2: Active → Authenticated — right side straight down ─────────────────────
arr(ACX+0.5, ACY-AH/2, AUX+0.5, AUY+AH/2,
    lbl='authenticate()\n[checkPassword(pw) = true] /\npw:=ui.askForPassword();\nuser.checkPassword(pw);\nauthTime:=time(); return true',
    lx=15.5, ly=17.2, fs=8.5, fc='#eaf4ea')

# ── T3: Active → Locked (wrong pw) — far-left arc ────────────────────────────
arr(ACX-2.4, ACY-AH/2, LKX+1.4, LKY+LH/2, rad=-0.35,
    lbl='authenticate()\n[checkPassword(pw) = false] /\npw:=ui.askForPassword();\nui.lockScreen(); return false',
    lx=0.9, ly=17.5, fs=8.2, fc='#fce8e8')

# ── T4: Active → Locked (manual lock) — arc just right of T3 ─────────────────
arr(ACX-2.0, ACY-AH/2-0.05, LKX+0.8, LKY+LH/2-0.05, rad=-0.15,
    lbl='lock()',
    lx=2.8, ly=16.1, fs=9.5, fc='white')

# ── T5: Active → Final — far-left long arc ────────────────────────────────────
arr(ACX-AW/2, ACY+0.3, FX-0.7, FY+0.36, rad=0.42,
    lbl='close() /\nSession destroyed',
    lx=0.8, ly=12.0, fs=8.5)

# ── T6: Authenticated self-loop — within 15 min ───────────────────────────────
self_loop(AUX, AUY+0.45, 'right',
          lbl='authenticate()\n[time()-authTime < 15] /\nreturn true',
          lx=18.0, ly=14.6, fs=8.2, yoff=0.48)

# ── T7: Authenticated self-loop — >=15 min, correct pw ───────────────────────
self_loop(AUX, AUY-0.45, 'right',
          lbl='authenticate()\n[time()-authTime >= 15,\ncheckPassword(pw) = true] /\npw:=ui.askForPassword();\nauthTime:=time(); return true',
          lx=18.0, ly=12.5, fs=8.0, yoff=0.48)

# ── T8: Authenticated → Locked (>=15 min, wrong pw) — upper horizontal ────────
arr(AUX-AW/2, AUY+0.3, LKX+LW/2, LKY+0.3,
    lbl='authenticate()\n[time()-authTime >= 15,\ncheckPassword(pw) = false] /\npw:=ui.askForPassword();\nui.lockScreen(); return false',
    lx=6.3, ly=14.9, fs=8.2, fc='#fce8e8')

# ── T9: Authenticated → Locked (manual lock) — lower horizontal ───────────────
arr(AUX-AW/2, AUY-0.3, LKX+LW/2, LKY-0.3,
    lbl='lock()',
    lx=6.3, ly=12.1, fs=9.5, fc='white')

# ── T10: Authenticated → Final ────────────────────────────────────────────────
arr(AUX-0.5, AUY-AH/2, FX-0.5, FY+0.36,
    lbl='close() /\nSession destroyed',
    lx=8.0, ly=9.0, fs=8.5)

# ── T11: Locked → Active — arcs up and right ─────────────────────────────────
arr(LKX+1.8, LKY+LH/2, ACX-2.0, ACY-AH/2, rad=-0.22,
    lbl='unlock() /\nauthTime := -1',
    lx=7.5, ly=17.6, fs=8.8, fc='#eaf4ea')

# ── T12: Locked → Final ───────────────────────────────────────────────────────
arr(LKX+0.5, LKY-LH/2, FX-1.8, FY+0.36, rad=0.18,
    lbl='close() /\nSession destroyed',
    lx=3.5, ly=8.5, fs=8.5)

# ── title ─────────────────────────────────────────────────────────────────────
ax.text(10.0, 23.75,
        'UML State Machine Diagram — Session Class',
        ha='center', va='center', fontsize=15, fontweight='bold')

plt.tight_layout(pad=0.2)
plt.savefig('/home/user/linkedin-outreach-/output/state_machine.png',
            dpi=160, bbox_inches='tight', facecolor='white')
print("Done.")
