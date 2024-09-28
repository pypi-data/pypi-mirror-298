from dataclasses import dataclass, field
from re import findall
from j2gpt.tcp import client
from typing import Callable, NoReturn

RESPONSE: str | None = None

def _load_template(path: str) -> str:
    with open(file=path, mode='r', encoding='UTF-8') as j2_file:
        return j2_file.read()

def _get_vars(j2: str) -> dict[str, str]:
    pattern: str = r'(?<!\\){%[ \n]*[_a-zA-Z][_a-zA-Z0-9]*[ \n]*[^\\]%}'
    matches: list[str] = findall(pattern=pattern, string=j2)
    return { var[2:-2].strip(): var for var in matches }

def _substitute(j2: str,
                subs: dict[str, str],
                vars: dict[str, str]) -> str:
    result: str = j2
    for name, sub in subs.items():
        result = result.replace(vars[name], sub)
    return result

@dataclass(slots=True)
class J2:
    base_path: str | None
    host: str = 'localhost'
    port: int = 50027
    _callback: Callable[[str], NoReturn] = field(init=False)

    def __post_init__(self) -> None:
        def callback(response: str) -> NoReturn:
            global RESPONSE
            RESPONSE = response
            exit(code=0)
        self._callback = callback

    def _assemble_template(self,
                           name: str,
                           subs: dict[str, str]) -> str:
        template: str = _load_template(path=f'{self.base_path}\\{name}.j2')
        vars: dict[str, str] = _get_vars(j2=template)
        prompt: str = _substitute(j2=template, subs=subs, vars=vars)
        return prompt

    def _ask(self, prompt: str) -> str:
        with client(on_receive=self._callback,
                    timeout=None,
                    host=self.host,
                    port=self.port) as clt:
            clt.send(message=prompt)
        global RESPONSE
        while True:
            if RESPONSE is not None:
                response: str = RESPONSE
                RESPONSE = None
                return response

    def ask(self, task: str, vars: dict[str, str]) -> str:
        prompt: str = self._assemble_template(name=task, subs=vars)
        return self._ask(prompt=prompt)
    
    def get(self, task: str, vars: dict[str, str]) -> str:
        return self._assemble_template(name=task, subs=vars)