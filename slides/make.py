"""
Pandoc Markdown to PDF Compiler with Watchdog Watch Mode

Replaces the polling loop in make.py with watchdog-based file system events.

Always watches:
  - slides.md (the file being compiled)
  - ../defaults.yaml
  - ../disclaimer.tex
  - references.bib  (same dir as slides.md)
  - imgs/           (same dir as slides.md)
  - code/           (same dir as slides.md, may not exist)

Usage
-----
Single compilation:
    $ python make2.py lecture01/slides.md

Watch mode:
    $ python make2.py lecture01/slides.md --watch

Dependencies
------------
    pip install watchdog
"""

import os
import contextlib
import argparse
import re
import tempfile
import threading
import time
from datetime import datetime

import sh
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SYNTAX_HIGHLIGHT = [
    "pygments",
    "tango",
    "espresso",
    "zenburn",
    "kate",
    "monochrome",
    "breezedark",
    "haddock",
]

pandoc = sh.Command("pandoc")


def _pandoc_version():
    version_output = pandoc(version=True)
    version_line = version_output.splitlines()[0]
    version_string = version_line.split()[-1]
    version_list = []
    for part in version_string.split("."):
        if part.isdigit():
            part = int(part)
        version_list.append(part)
    return tuple(version_list)


PANDOC_VERSION = _pandoc_version()

PANDOC_CMD_TEMPLATE = pandoc.bake(
    t="beamer",
    d="../defaults.yaml",
    highlight_style="../sh_style.theme",
    verbose=True,
)

if PANDOC_VERSION < (2, 11):
    PANDOC_CMD_TEMPLATE = PANDOC_CMD_TEMPLATE.bake(filter="pandoc-citeproc")
else:
    PANDOC_CMD_TEMPLATE = PANDOC_CMD_TEMPLATE.bake(citeproc=True)


RX_INCLUDE_DIRECTIVE = re.compile(r"!!include\s+([a-zA-Z0-9+#-]+):\s*(.+)")

REPLACES = {
    "≠": r"$\neq$",
    "λ": r"$\lambda$",
    "η": r"$\eta$",
    "θ": r"$\theta$",
    "α": r"$\alpha$",
    "ⱼ": r"$_{j}$",
}

RENDER_FROM_HERE = r"\\RENDER FROM HERE\\"


@contextlib.contextmanager
def chdir(newdir):
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def find_last_index_second_dash_line(src):
    current_position = 0
    found_first_dash_line = False
    for line in src.splitlines():
        current_position += len(line) + 1
        line = line.strip()
        if line.replace("-", "") == "":
            if found_first_dash_line:
                return current_position
            found_first_dash_line = True
    return -1


def render_include_to_markdown(target):
    match = RX_INCLUDE_DIRECTIVE.search(target) if isinstance(target, str) else target
    lang = match.group(1).lower()
    path = match.group(2).strip()
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f"```{lang}\n{f.read()}\n```"
    except Exception as err:
        print(f"WARNING: Failed to include '{path}': {err}")
        content = f"**ERROR: could not include `{path}`: {err}**"
    return content


def preprocess_markdown_source(src, fname, tempdir):
    output_path = os.path.join(tempdir, fname)

    if RENDER_FROM_HERE in src:
        yaml_end = find_last_index_second_dash_line(src)
        marker_end = src.index(RENDER_FROM_HERE) + len(RENDER_FROM_HERE)
        src = src[:yaml_end] + src[marker_end:]

    for char, replacement in REPLACES.items():
        src = src.replace(char, replacement)

    src = RX_INCLUDE_DIRECTIVE.sub(render_include_to_markdown, src)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(src)

    return output_path


def run_pandoc(path, output_path, ignore_error):
    pandoc = PANDOC_CMD_TEMPLATE.bake(path, output=output_path)
    print(pandoc)
    try:
        return pandoc()
    except sh.ErrorReturnCode as err:
        if ignore_error:
            print("=======================")
            print(">>> IGNORING ERROR <<<")
            print("=======================")
            print(err)
        else:
            raise


class ChangeHandler(FileSystemEventHandler):
    """Watchdog event handler that triggers recompilation on relevant changes."""

    def __init__(self, trigger, watched_files, watched_dirs):
        """
        Parameters
        ----------
        trigger : threading.Event
            Set when a relevant change is detected.
        watched_files : list of str
            Absolute paths to individual files to watch.
        watched_dirs : list of str
            Absolute paths to directories; any change inside triggers recompile.
            Non-existent directories are still registered (handles code/ being created).
        """
        super().__init__()
        self.trigger = trigger
        self.watched_files = {os.path.abspath(p) for p in watched_files}
        self.watched_dirs = [os.path.abspath(d) for d in watched_dirs]

    def _is_relevant(self, path):
        abs_path = os.path.abspath(path)
        if abs_path in self.watched_files:
            return True
        return any(abs_path.startswith(d + os.sep) for d in self.watched_dirs)

    def _handle(self, event):
        if not event.is_directory and self._is_relevant(event.src_path):
            rel = os.path.relpath(event.src_path)
            print(f"  [watchdog] {event.event_type}: {rel}")
            self.trigger.set()

    on_modified = _handle
    on_created = _handle
    on_deleted = _handle


def get_parser():
    parser = argparse.ArgumentParser(
        description="Pandoc Beamer compiler with watchdog-based watch mode"
    )
    parser.add_argument("archivo", help="path to slides.md", type=str)
    parser.add_argument(
        "-w", "--watch", help="watch mode", action="store_true", default=False
    )
    parser.add_argument("-i", "--ignore_error", action="store_false", default=True)
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument(
        "--debounce",
        help="seconds to wait after a change before recompiling (default: 0.3)",
        type=float,
        default=0.3,
    )
    return parser


def main():
    args = get_parser().parse_args()

    original_path = args.archivo
    watch = args.watch
    ignore_error = args.ignore_error
    verbose = args.verbose
    debounce = args.debounce

    # Resolve absolute paths
    lecture_dir = os.path.abspath(os.path.dirname(original_path)) or os.getcwd()
    slides_file = os.path.basename(original_path)
    parent_dir = os.path.dirname(
        lecture_dir
    )  # where defaults.yaml / disclaimer.tex live

    abs_slides = os.path.join(lecture_dir, slides_file)
    abs_output = os.path.join(lecture_dir, slides_file.replace(".md", ".pdf"))

    watched_files = [
        abs_slides,
        os.path.join(parent_dir, "defaults.yaml"),
        os.path.join(parent_dir, "disclaimer.tex"),
        os.path.join(lecture_dir, "references.bib"),
    ]
    watched_dirs = [
        os.path.join(lecture_dir, "imgs"),
        os.path.join(lecture_dir, "codes"),  # may not exist
    ]

    def compile_once():
        src = read_file(abs_slides)
        now = datetime.now().strftime("%H:%M:%S")
        partial = "[Partial Rendering]" if RENDER_FROM_HERE in src else ""
        suffix = f" {partial}" if partial else ""
        print(f"[{now}] Compiling {original_path} -> {abs_output}{suffix}")
        # Run pandoc from lecture_dir so ../defaults.yaml resolves correctly
        with chdir(lecture_dir), tempfile.TemporaryDirectory() as tempdir:
            processed = preprocess_markdown_source(src, slides_file, tempdir)
            import shutil; shutil.copy(processed, "coso.md")
            result = run_pandoc(processed, abs_output, ignore_error)
        if verbose and result:
            print(result)

    # Initial compilation
    compile_once()

    if not watch:
        return

    # --- Watchdog setup ---
    trigger = threading.Event()
    handler = ChangeHandler(trigger, watched_files, watched_dirs)
    observer = Observer()

    # Watch lecture dir recursively (catches slides.md, references.bib, imgs/, code/)
    observer.schedule(handler, lecture_dir, recursive=True)
    # Watch parent dir non-recursively (defaults.yaml, disclaimer.tex)
    observer.schedule(handler, parent_dir, recursive=False)

    sep = "=" * 62
    print(sep)
    print("Watching for changes (Ctrl+C to stop)")
    print("  Files:")
    for f in watched_files:
        status = "" if os.path.exists(f) else "  [not found]"
        print(f"    {f}{status}")
    print("  Directories:")
    for d in watched_dirs:
        status = "" if os.path.isdir(d) else "  [does not exist]"
        print(f"    {d}{status}")
    print(sep)

    observer.start()
    try:
        while True:
            if trigger.wait(timeout=1.0):
                trigger.clear()
                time.sleep(debounce)
                trigger.clear()  # discard events that arrived during debounce
                compile_once()
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
