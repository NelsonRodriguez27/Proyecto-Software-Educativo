from pathlib import Path
import re


CSS_BLOCK = """
    .side-chat{display:none !important}
    .game-gauss-chat-wrapper{position:fixed;right:18px;bottom:24px;z-index:80;display:none;flex-direction:column;align-items:flex-end;gap:12px;width:fit-content;pointer-events:none}
    #screenGame.active ~ .game-gauss-chat-wrapper{display:flex}
    .game-gauss-bubble{max-width:280px;background:#fff;color:#333;border-radius:18px;padding:14px 16px;box-shadow:0 10px 30px rgba(0,0,0,.18);font-size:15px;line-height:1.4;position:relative;opacity:0;transform:translateY(15px) scale(.95);pointer-events:none;transition:opacity .35s ease,transform .35s ease;border:2px solid rgba(226,188,51,.28)}
    .game-gauss-bubble.show{opacity:1;transform:translateY(0) scale(1);pointer-events:auto}
    .game-gauss-bubble::after{content:"";position:absolute;right:44px;bottom:-8px;width:16px;height:16px;background:#fff;transform:rotate(45deg);border-radius:3px;border-right:2px solid rgba(226,188,51,.18);border-bottom:2px solid rgba(226,188,51,.18)}
    .game-gauss-title{font-weight:700;color:var(--gauss-orange);margin-bottom:4px;font-size:16px}
    .game-gauss-chat-btn{width:180px;height:180px;border:none;border-radius:50%;background:linear-gradient(135deg,#E2BC33,#C25C26);box-shadow:0 10px 24px rgba(0,0,0,.22);cursor:pointer;display:flex;align-items:center;justify-content:center;overflow:hidden;pointer-events:auto;transition:transform .25s ease,box-shadow .25s ease;flex-shrink:0;padding:0;animation:gaussFloatGame 2.8s ease-in-out infinite}
    .game-gauss-chat-btn:hover,.game-gauss-chat-btn:focus-visible{transform:scale(1.06);box-shadow:0 14px 28px rgba(0,0,0,.28);outline:none}
    .game-gauss-chat-btn img{width:100%;height:100%;object-fit:cover;object-position:center top;border-radius:50%}
    .game-gauss-chat-btn.open{animation:none;transform:scale(1.04);box-shadow:0 0 0 6px rgba(226,188,51,.18),0 14px 30px rgba(0,0,0,.26)}
    .game-gauss-chat-btn.is-speaking{animation:none;transform:scale(1.08);box-shadow:0 0 0 8px rgba(115,162,29,.22),0 0 22px rgba(226,188,51,.32),0 16px 34px rgba(0,0,0,.28)}
    @keyframes gaussFloatGame{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
    @media(max-width:980px){.game-gauss-chat-wrapper{right:14px;bottom:14px}.game-gauss-chat-btn{width:100px;height:100px}.game-gauss-bubble{max-width:230px;font-size:14px}}
    @media(max-width:640px){.game-gauss-chat-wrapper{right:10px;bottom:10px}.game-gauss-chat-btn{width:90px;height:90px}.game-gauss-bubble{max-width:200px;font-size:13px;padding:12px 13px}.game-gauss-bubble::after{right:28px}}
    @media(max-width:420px){.game-gauss-chat-btn{width:80px;height:80px}.game-gauss-bubble{max-width:180px;font-size:12.5px}}
"""


HTML_BLOCK = """

    <div class="game-gauss-chat-wrapper" id="gameGaussWrapper">
      <div class="game-gauss-bubble" id="gameGaussBubble" role="status" aria-live="polite">
        <div class="game-gauss-title" id="gameGaussBubbleTitle">¡Hola! Soy Gauss 👋</div>
        <div id="gameGaussBubbleText">Estoy aquí para ayudarte en cada ejercicio.</div>
      </div>
      <button class="game-gauss-chat-btn" id="gameGaussBtn" aria-label="Abrir o cerrar el asistente Gauss" aria-expanded="false" type="button">
        <img src="../../imagenes/Gauss.png" id="gameGaussBtnImg" data-idle-src="../../imagenes/Gauss.png" data-speaking-src="../../imagenes/gauss2.gif" data-fallback-src="../../imagenes/gauss1.gif" alt="" aria-hidden="true" onerror="if(this.dataset.fallbackApplied!=='1'){this.dataset.fallbackApplied='1';this.src=this.dataset.fallbackSrc||'../../imagenes/gauss1.gif';}else{this.style.display='none';this.parentElement.innerHTML+='<div style=\\'font-size:3.5rem\\'>🦉</div>'; }">
      </button>
    </div>
"""


HELPER_BLOCK = """

function updateGameGaussBubble(texto, titulo='Gauss te orienta 🦉') {
  if (!gameGaussBubbleText || !gameGaussBubbleTitle) return;
  gameGaussBubbleTitle.textContent = titulo;
  gameGaussBubbleText.textContent = texto || 'Estoy aquí para ayudarte en cada ejercicio.';
  gameGaussLastMessage = texto || 'Estoy aquí para ayudarte en cada ejercicio.';
}

function showGameGaussBubble(ms=4500) {
  if (!gameGaussBubble || !gameGaussBtn) return;
  if (gameGaussHideTimer) {
    clearTimeout(gameGaussHideTimer);
    gameGaussHideTimer = null;
  }
  gameGaussBubble.classList.add('show');
  gameGaussBtn.classList.add('open');
  gameGaussBtn.setAttribute('aria-expanded', 'true');
  if (typeof ms === 'number' && ms > 0) gameGaussHideTimer = setTimeout(hideGameGaussBubble, ms);
}

function hideGameGaussBubble() {
  if (!gameGaussBubble || !gameGaussBtn) return;
  if (gameGaussHideTimer) {
    clearTimeout(gameGaussHideTimer);
    gameGaussHideTimer = null;
  }
  gameGaussBubble.classList.remove('show');
  gameGaussBtn.classList.remove('open');
  gameGaussBtn.setAttribute('aria-expanded', 'false');
}

function setGameGaussSpeaking(on) {
  if (!gameGaussBtn) return;
  gameGaussBtn.classList.toggle('is-speaking', !!on);
  if (gameGaussBtnImg) {
    const idle = gameGaussBtnImg.dataset.idleSrc || gameGaussBtnImg.src;
    const speakingSrc = gameGaussBtnImg.dataset.speakingSrc || idle;
    gameGaussBtnImg.src = on ? speakingSrc : idle;
  }
}

function initGameGauss() {
  if (!gameGaussBtn || !gameGaussBubble) return;
  updateGameGaussBubble(gameGaussLastMessage, '¡Hola! Soy Gauss 👋');
  gameGaussBtn.addEventListener('click', () => {
    const open = gameGaussBubble.classList.contains('show');
    if (open) {
      hideGameGaussBubble();
      return;
    }
    updateGameGaussBubble(gameGaussLastMessage, '¡Hola! Soy Gauss 👋');
    showGameGaussBubble(4000);
  });
}
"""


CONST_BLOCK = """const gameGaussBubble = document.getElementById('gameGaussBubble');
const gameGaussBubbleTitle = document.getElementById('gameGaussBubbleTitle');
const gameGaussBubbleText = document.getElementById('gameGaussBubbleText');
const gameGaussBtn = document.getElementById('gameGaussBtn');
const gameGaussBtnImg = document.getElementById('gameGaussBtnImg');"""


STATE_BLOCK = """let gameGaussHideTimer = null;
let gameGaussLastMessage = 'Estoy aquí para ayudarte en cada ejercicio.';"""


def inject_into_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = text.replace("/* TEST_MARK_GAUSS */", "")

    if "game-gauss-chat-wrapper" not in text:
        text = text.replace("</style>", CSS_BLOCK + "\n  </style>", 1)
        text = text.replace(
            '<section class="screen" id="screenResult">',
            HTML_BLOCK + '\n    <section class="screen" id="screenResult">',
            1,
        )

    if "const gameGaussBubble" not in text:
        text = re.sub(
            r"(const owlResult\s*=\s*document\.getElementById\('owlResult'\);)",
            r"\1\n" + CONST_BLOCK,
            text,
            count=1,
        )

    if "gameGaussHideTimer" not in text:
        text = re.sub(
            r"(let audioCtx\s*=\s*null;)",
            r"\1\n" + STATE_BLOCK,
            text,
            count=1,
        )

    if "function updateGameGaussBubble" not in text:
        text = text.replace(
            "function activarHabla()",
            HELPER_BLOCK + "\nfunction activarHabla()",
            1,
        )

    text = re.sub(
        r"function activarHabla\(\)\s*\{\s*\[owlWelcome,\s*owlSide,\s*owlResult\]\.forEach\(el => \{\s*if\s*\(el\)\s*el\.classList\.add\(\"talking\"\);\s*\}\);\s*\}",
        'function activarHabla() { [owlWelcome, owlSide, owlResult].forEach(el => { if (el) el.classList.add("talking"); }); setGameGaussSpeaking(true); }',
        text,
        count=1,
    )
    text = re.sub(
        r"function desactivarHabla\(\)\s*\{\s*\[owlWelcome,\s*owlSide,\s*owlResult\]\.forEach\(el => \{\s*if\s*\(el\)\s*el\.classList\.remove\(\"talking\"\);\s*\}\);\s*\}",
        'function desactivarHabla() { [owlWelcome, owlSide, owlResult].forEach(el => { if (el) el.classList.remove("talking"); }); setGameGaussSpeaking(false); }',
        text,
        count=1,
    )

    text = re.sub(
        r"if\s*\(target\s*===\s*'side'\)\s*\{\s*escribirSide\(texto\);\s*\}",
        "if (target === 'side') { escribirSide(texto); updateGameGaussBubble(texto, 'Gauss te orienta 🦉'); showGameGaussBubble(5000); }",
        text,
        count=1,
    )
    text = re.sub(
        r"if\s*\(targetElId\s*===\s*'side'\)\s*\{\s*escribirSide\(texto\);\s*\}",
        "if (targetElId === 'side') { escribirSide(texto); updateGameGaussBubble(texto, 'Gauss te orienta 🦉'); showGameGaussBubble(5000); }",
        text,
        count=1,
    )

    if "initGameGauss();" not in text:
        text = re.sub(
            r'(window\.addEventListener\("load"[^\n]*\);)',
            r"\1\ninitGameGauss();",
            text,
            count=1,
        )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    root = Path(__file__).resolve().parents[1] / "Juegos"
    files = sorted(root.rglob("*.html"))
    changed = []
    for path in files:
        if inject_into_file(path):
            changed.append(path)
    print(f"changed {len(changed)} files")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
