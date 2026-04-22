from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1] / "Juegos"


MISSING_STATE = [
    ROOT / "Juegos_Unidad1" / "UNIDAD_01_JUEGO_01.html",
    ROOT / "Juegos_Unidad1" / "UNIDAD_01_JUEGO_02.html",
    ROOT / "Juegos_Unidad1" / "UNIDAD_01_JUEGO_03.html",
    ROOT / "Juegos_Unidad1" / "UNIDAD_01_JUEGO_04.html",
    ROOT / "Juegos_Unidad1" / "UNIDAD_01_JUEGO_05.html",
    ROOT / "Juegos_Unidad2" / "UNIDAD_02_JUEGO_06.html",
    ROOT / "Juegos_Unidad4" / "UNIDAD_04_ JUEGO_17.html",
    ROOT / "Juegos_Unidad4" / "UNIDAD_04_ JUEGO_18.html",
]


MISSING_SPEAK = [
    ROOT / "Juegos_Unidad1" / "UNIDAD_01_JUEGO_01.html",
    ROOT / "Juegos_Unidad1" / "UNIDAD_01_JUEGO_02.html",
    ROOT / "Juegos_Unidad1" / "UNIDAD_01_JUEGO_03.html",
    ROOT / "Juegos_Unidad1" / "UNIDAD_01_JUEGO_04.html",
    ROOT / "Juegos_Unidad1" / "UNIDAD_01_JUEGO_05.html",
    ROOT / "Juegos_Unidad2" / "UNIDAD_02_JUEGO_06.html",
]


def patch_state(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "let gameGaussHideTimer" in text and "let gameGaussLastMessage" in text:
        return False

    pattern = r"(let\s+speakingNow\s*=\s*false[^;\n]*;\s*let\s+audioCtx\s*=\s*null;)"
    repl = r"\1\nlet gameGaussHideTimer = null;\nlet gameGaussLastMessage = 'Estoy aquí para ayudarte en cada ejercicio.';"
    new_text, count = re.subn(pattern, repl, text, count=1)
    if count == 0:
        pattern = r"(let\s+audioCtx\s*=\s*null;)"
        repl = r"\1\nlet gameGaussHideTimer = null;\nlet gameGaussLastMessage = 'Estoy aquí para ayudarte en cada ejercicio.';"
        new_text, count = re.subn(pattern, repl, text, count=1)
    if count:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def patch_speaking(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = re.sub(
        r'function activarHabla\(\)\s*\{\s*\[owlWelcome,\s*owlSide,\s*owlResult\]\.forEach\((?:function\(el\)|el =>)\s*\{\s*if\s*\(el\)\s*el\.classList\.add\("talking"\);\s*\}\);\s*\}',
        'function activarHabla() { [owlWelcome, owlSide, owlResult].forEach(function(el){ if(el) el.classList.add("talking"); }); setGameGaussSpeaking(true); }',
        text,
        count=1,
    )
    text = re.sub(
        r'function desactivarHabla\(\)\s*\{\s*\[owlWelcome,\s*owlSide,\s*owlResult\]\.forEach\((?:function\(el\)|el =>)\s*\{\s*if\s*\(el\)\s*el\.classList\.remove\("talking"\);\s*\}\);\s*\}',
        'function desactivarHabla() { [owlWelcome, owlSide, owlResult].forEach(function(el){ if(el) el.classList.remove("talking"); }); setGameGaussSpeaking(false); }',
        text,
        count=1,
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in MISSING_STATE:
        if patch_state(path):
            changed.append(path)
    for path in MISSING_SPEAK:
        if patch_speaking(path) and path not in changed:
            changed.append(path)
    print(f"fixed {len(changed)} files")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
