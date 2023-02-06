import sys
import re
from pathlib import Path



def pure_root_dir(source: str) -> Path:
    path = Path(source).absolute()
    if not path.exists():
        return None
    if not path.is_dir():
        path = path.parent
    return path


def get_bandcamp_music(dir: Path):
    files = dir.glob(pattern="*.*")
    for file in files:
        matched = re.match(".*? - .*? - (.*?)\.(.*)", file.name)
        if not matched:
            continue
        name, extension = matched.groups()
        file_new_name = f"{name}.{extension}"
        return file_new_name


def get_dir_files(dir: Path):
    return dir.glob(pattern="*.*")


def fetch_bandcamp_album(dir: Path):
    return re.match(pattern="(.*) - (.*)", string=dir.name)


def fetch_bandcamp_soundtrack(file: Path):
    return re.match(pattern=".*? - .*? - (.*?)\.(.*)", string=file.name)


def run(source: str):
    source_dir = pure_root_dir(source=source)
    if not source_dir:
        return None
    
    fetched_album = fetch_bandcamp_album(dir=source_dir)
    if not fetched_album:
        return None

    files = get_dir_files(source_dir)
    for soundtrack in files:
        fetched_soundtrack = fetch_bandcamp_soundtrack(soundtrack)
        if not fetched_soundtrack:
            continue
        soundtrack_src_name, soundtrack_src_extension = fetched_soundtrack.groups()
        soundtrack_dst_name = f"{soundtrack_src_name}.{soundtrack_src_extension}"
        soundtrack_dst_path = source_dir.joinpath(soundtrack_dst_name)
        soundtrack.rename(soundtrack_dst_path)
        print(f"{soundtrack} -> {soundtrack_dst_path}")



if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else __file__
    run(source)