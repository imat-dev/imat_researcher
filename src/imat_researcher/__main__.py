"""Console entry point: `imat-researcher` or `python -m imat_researcher`."""

import argparse
import logging


def main() -> None:
    parser = argparse.ArgumentParser(prog="imat-researcher", description=__doc__)
    parser.add_argument(
        "--simple",
        action="store_true",
        help="launch the unstyled interface instead of the styled one",
    )
    parser.add_argument("--host", default=None, help="server name to bind")
    parser.add_argument("--port", type=int, default=None, help="server port to bind")
    parser.add_argument("--share", action="store_true", help="create a public Gradio link")
    parser.add_argument(
        "--log-level", default="INFO", help="logging level (default: INFO)"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level.upper(),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )

    if args.simple:
        from imat_researcher.ui import simple as frontend
    else:
        from imat_researcher.ui import app as frontend

    launch_kwargs = {"share": args.share}
    if args.host is not None:
        launch_kwargs["server_name"] = args.host
    if args.port is not None:
        launch_kwargs["server_port"] = args.port

    frontend.launch(**launch_kwargs)


if __name__ == "__main__":
    main()
