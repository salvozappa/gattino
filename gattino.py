from kitty.boss import Boss # type: ignore
import subprocess

def main(args: list[str]) -> str:
    # https://www.asciiart.eu/animals/cats
    # http://patorjk.com/software/taag/#p=display&f=Calvin%20S&t=gattino
    print(""" _._     _,-'""`-._
(,-.`._,'(       |\\`-/|
    `-.-' \\ )-`( , o o)
          `-    \\`_`"'-

┌─┐┌─┐┌┬┐┌┬┐┬┌┐┌┌─┐
│ ┬├─┤ │  │ │││││ │
└─┘┴ ┴ ┴  ┴ ┴┘└┘└─┘

Explain in plain English the command you want to execute.
""")

    human_language_command = input('> ')
    prompt = f"""
You will be given an action in human language to be executed on a bash shell.
Please generate a single line bash command that executes the action.
ATTENTION: please fence the command using a code block

Action to execute: {human_language_command}
"""
    print("PROMPT:")
    print(prompt)
    with open('/tmp/gattino_prompt.txt', 'w') as file:
        file.write(human_language_command + '\n')
    model_output = run_command(f'/usr/local/bin/ollama run codellama '' --nowordwrap < /tmp/gattino_prompt.txt')
    return model_output

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")
        return None

def handle_result(args: list[str], answer: str, target_window_id: int, boss: Boss) -> None:
    # get the kitty window into which to paste answer
    w = boss.window_id_map.get(target_window_id)
    if w is not None:
        w.paste_text(answer)
