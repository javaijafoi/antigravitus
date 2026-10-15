from pathlib import Path
import re


class CommandBook:
    """Read the live-help dictionary; never promote a generic manual into a tested command."""

    def __init__(self,path):
        self.path=Path(path)
        self.entries={}
        if self.path.is_file():
            value=self.path.read_text(encoding='utf-8-sig')
            for match in re.finditer(r'(?ms)^## `([^`]+)`\s*\n(.*?)(?=^## `|\Z)',value):
                self.entries[match[1]]=match[2]

    def has(self,verb):
        body=self.entries.get(verb,'')
        return bool(re.search(r'\*\*Listado:\*\*\s*sim\b',body,re.I))

    def require(self,verb):
        if not self.has(verb):raise ValueError('Comando sem confirmação na lista do dicionário: '+verb)
        return self.entries[verb]

    def lookup(self,verb):
        return self.entries.get(verb,'')

    def validate_command(self,command):
        if any(c in command for c in ('\n','\r',';','\x00')):raise ValueError('Ação deve enviar um único comando.')
        verb=command.split()[0] if command.strip() else ''
        if verb:self.require(verb)
        return command
