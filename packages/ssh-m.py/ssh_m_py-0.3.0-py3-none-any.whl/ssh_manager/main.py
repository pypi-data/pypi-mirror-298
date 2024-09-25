from os import environ
from importlib.metadata import version

from .parse_args import parse_mode
from .routing import routing


def main():
    """Entrypoint for `setup.py`

    :return: No, lol.
    """
    print(f"ssh_manager "
          f"v{version('ssh_m.py') if not environ.get('SSH_M_PREVIEW_MODE') else '0.x.y'}:\n"
          )
    try:
        routing(parse_mode().n)
    except KeyboardInterrupt:
        raise SystemExit('\n')


if __name__ == "__main__":
    main()
