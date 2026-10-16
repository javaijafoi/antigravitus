"""Valida e prepara uma revisão única. Só --publish cria commit; só --push envia."""
import argparse
from pathlib import Path, PurePosixPath
import subprocess
import sys
from scripts.check_project import validate_project

BASE_DIR = Path(__file__).resolve().parent
ROOT_FILES = {"index.html", "ficha.html", "mapa.html", "sobre.html", "README.md",
              "TEMPLATE_NOVO_HEROI.md", "vercel.json", "add_day.py", "add_chapter.py",
              "create_hero.py", "publish_daily.py", ".gitignore"}
ALLOWED = {"data": {".json", ".md"}, "css": {".css"}, "js": {".js"},
           "scripts": {".py", ".md"}, "skills": {".md", ".py", ".json"},
           "docs": {".md"},
           "automato": {".py", ".md", ".json"},
           "audio": {".json", ".mp3", ".wav", ".ogg", ".m4a"}}


def public_path(path):
    """Lista explícita, além do .gitignore, impede enviar sessões ou credenciais."""
    parts = PurePosixPath(path).parts
    if not parts or ".." in parts:
        return False
    lowered = [part.lower() for part in parts]
    name = lowered[-1]
    if any(part.startswith(".") for part in parts) and path != ".gitignore":
        return False
    if any(part in {"local", "work", "node_modules", "__pycache__", "test_samples"} for part in lowered):
        return False
    if any(word in name for word in ("credential", "password", "secret", "token", "session_")) or name.startswith(("play_dia", "mudclient")):
        return False
    if path in ROOT_FILES:
        return True
    return parts[0] in ALLOWED and PurePosixPath(path).suffix.lower() in ALLOWED[parts[0]]


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True,
                          encoding="utf-8", errors="replace").stdout


def changed_files(root):
    tracked = git(root, "diff", "--no-renames", "--name-only", "-z", "HEAD").split("\0")
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z").split("\0")
    candidates = sorted(set(path for path in tracked + untracked if path))
    return [path for path in candidates if public_path(path)], [path for path in candidates if not public_path(path)]


def sync_all(root=BASE_DIR, *, publish=False, push=False, message="Atualiza crônicas e registros documentais"):
    root = Path(root).resolve()
    if push and not publish:
        raise ValueError("--push exige --publish explícito.")
    errors, warnings = validate_project(root)
    for warning in warnings:
        print(f"[AVISO] {warning}")
    if errors:
        print("Publicação bloqueada por inconsistências documentais:")
        for error in errors:
            print(f"  {error}")
        return False
    try:
        git_root = Path(git(root, "rev-parse", "--show-toplevel").strip()).resolve()
        if git_root != root:
            raise ValueError("Execute no repositório deste projeto; um repositório ancestral não será publicado.")
        files, skipped = changed_files(root)
    except subprocess.CalledProcessError:
        if not publish:
            print("Simulação: registros validados. Esta cópia não é um checkout Git; nenhum commit ou envio foi feito.")
            return True
        raise ValueError("Publicação requer um checkout Git local com HEAD existente.")
    print(f"{'Publicação' if publish else 'Simulação'}: {len(files)} arquivo(s) da revisão:")
    for path in files:
        print(f"  {path}")
    if skipped:
        print(f"{len(skipped)} arquivo(s) fora da lista de publicação foram preservados e excluídos desta operação.")
    if not publish or not files:
        return True
    staged = git(root, "diff", "--cached", "--name-only", "-z")
    if staged.strip("\0"):
        raise ValueError("O índice Git já contém alterações preparadas. Preserve ou finalize essa revisão antes de publicar outra.")
    # Um único commit inclui apenas a revisão explicitamente listada. git add respeita .gitignore.
    git(root, "add", "--", *files)
    actual = set(git(root, "diff", "--cached", "--name-only", "-z").strip("\0").split("\0"))
    if actual != set(files):
        raise ValueError("O conjunto preparado mudou durante a operação. Confira o índice antes de continuar; nenhum commit foi criado.")
    git(root, "commit", "-m", message)
    print("Revisão registrada em um único commit local.")
    if push:
        git(root, "push")
        print("Commit enviado ao destino Git já configurado.")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true", help="Cria um único commit local após a validação.")
    parser.add_argument("--push", action="store_true", help="Envia pelo Git configurado; exige --publish.")
    parser.add_argument("--message", default="Atualiza crônicas e registros documentais")
    args = parser.parse_args()
    try:
        return 0 if sync_all(publish=args.publish, push=args.push, message=args.message) else 1
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
