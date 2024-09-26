import os, fnmatch, shutil
from logging import getLogger
from subprocess import check_call, CalledProcessError
import click
from tqdm import tqdm

@click.command()
@click.option("--pattern", "-p", required=True, multiple=True, help="Pattern to search files.")
@click.option("--source", "-s", default=[""], required=False, multiple=True, help="Source directory relative path")
@click.option("--destination", "-d", default="static", required=False, help="Directory where files will be copied to.")
@click.option("--exclude", "-e", default=[], required=False, multiple=True, help="Directory/directories to exclude.")
@click.option("--maintain-hierarchy", "-h", type=bool, default=True, required=False, help="If True then copied files will keep directory hierarchy relative to root dir")
@click.option("--respect-git-ignore", "-g", type=bool, default=True, required=False, help="If True then function will return False if given directory is ignored by git")
def collect_files_cli(
    pattern: list[str],
    source: list[str],
    destination: str,
    exclude: list[str],
    maintain_hierarchy: bool,
    respect_git_ignore: bool
):
    click.echo(click.style(
        f"Collecting files with {pattern} pattern{'s' if len(pattern)>1 else ''} to `{destination}` directory",
        fg='blue',
        bold=True
    ))
    click.echo(click.style(f"-- from source{'s' if len(source)>1 else ''} {source}", fg='cyan'))
    click.echo(click.style(f"-- excluding {exclude}", fg='cyan'))
    click.echo(click.style(f"-- {'' if maintain_hierarchy else 'not '}maintaining file hierarchy", fg='cyan'))
    click.echo(click.style(f"-- {'excluding' if respect_git_ignore else 'including'} git ignored files", fg='cyan'))
    
    collect_files(pattern, source, destination, exclude, maintain_hierarchy, respect_git_ignore)

def collect_files(
    patterns: str | list[str],
    src_dirs: str | list[str] = ".",
    dest: str | os.PathLike = "static",
    exclude_dir: str | list[str] = [],
    maintain_hierarchy: bool = True,
    respect_git_ignore: bool = True,
) -> bool:
    '''method  `collect_files`
    
    Args:
        patterns (str | list[str]): Pattern to search files.
        src_dirs (list[str]): List of source directory relative path.
        dest (str | os.PathLike): Directory where files will be copied to.
        exclude_dir (str | list[str]): Directory/directories to exclude.
        maintain_hierarchy (bool): If True then copied files will keep directory hierarchy relative to root dir
        respect_git_ignore (bool): If True then function will return False if given directory is ignored by git
    Returns:
        newFiles (list[os.PathLike]): List of new copied file paths in destination directory.
    :raises:
        AssertionError: If none of provided source directories exist or are all ignored by git
    '''
    rootDir = os.getcwd()
    click.echo(click.style(f"Root Dir (cwd): {rootDir}", fg='cyan'))
    destPath = os.path.join(rootDir, dest)
    if not os.path.exists(destPath):
        click.echo(click.style(f"Creating destination directory: {destPath}", fg='cyan'))
        os.makedirs(destPath, exist_ok=True)

    if not hasattr(exclude_dir, '__iter__'):
        exclude_dir = [exclude_dir]
    files = get_files(patterns, src_dirs, [destPath, *exclude_dir], respect_git_ignore)
    
    newFiles = []
    for file in tqdm(files, desc=f'Copying files to {destPath}', leave=None, colour="green"):
        newFiles.append(copy_file(file, destPath, maintain_hierarchy))
    click.echo(click.style(f"New files: {chr(10)}--> {f'{chr(10)}--> '.join(newFiles)}", fg='green'))
    return newFiles

def copy_file(file: os.PathLike, dest: os.PathLike, maintain_hierarchy: bool) -> os.PathLike:
    rootDir = os.getcwd()
    hierarchical_path = dest
    if maintain_hierarchy:
        fileDir = os.path.dirname(file)
        fileDir = "" if fileDir == rootDir else fileDir.split(os.path.join(rootDir, "/"))[-1]
        hierarchical_path = os.path.join(dest, fileDir)
        os.makedirs(hierarchical_path, exist_ok=True)
    return shutil.copy(file, hierarchical_path)

def get_files(
    patterns: str | list[str],
    src_dirs: str | list[str] = ".",
    exclude_dir: str | list[str] = "static",
    respect_git_ignore: bool = True,
) -> list[str]:
    '''method  `get_files`
    
    Args:
        patterns (str | list[str]): Pattern to search files.
        src_dirs (list[str]): List of source directory relative path
        exclude_dir (str | list[str]): directory/directories to exclude
        respect_git_ignore (bool): If True then function will return False if given directory is ignored by git
    Returns:
        files (list[os.PathLike]): List of file paths.
    :raises:
        AssertionError: If none of provided source directories exist or are all ignored by git
    '''
    if not hasattr(exclude_dir, '__iter__'):
        exclude_dir = [exclude_dir]
    exclude_dir = [os.path.abspath(path) for path in exclude_dir]
    
    if src_dirs == ".":
        src_dirs = [""]
    elif not hasattr(src_dirs, '__iter__'):
        src_dirs = [src_dirs]
    
    srcDirs = get_src_dirs(os.getcwd(), src_dirs, respect_git_ignore)
    assert len(srcDirs) > 0, f"Invalid source {'directories' if len(src_dirs) > 1 else 'directory'}"
    if not hasattr(patterns, '__iter__'):
        patterns = [patterns]
    
    srcFiles = []
    for src_dir in tqdm(srcDirs, desc="Collect valid source directories", colour="green"):
        for (dirpath, dirnames, filenames) in os.walk(src_dir):
            if dirpath in exclude_dir or (respect_git_ignore and is_ignored(dirpath)):
                pop_all(dirnames)
                continue
            srcFiles.extend([os.path.join(dirpath, file) for file in filenames])
    files = []
    for pattern in patterns:
        files.extend(fnmatch.filter(srcFiles, f'*{pattern}*'))
    click.echo(click.style(f"Matching files: {chr(10)}--> {f'{chr(10)}--> '.join(files)}", fg='yellow'))
    return files

def pop_all(li: list) -> list:
    '''method `pop_all`, returns same emptied list'''
    r, li[:] = li[:], []
    return r

def get_src_dirs(
    root_dir: os.PathLike,
    src_dirs: list[str],
    respect_git_ignore: bool = True
)-> list[None | os.PathLike]:
    '''method `get_src_dirs`
    Args:
        root_dir (os.PathLike): base absolute path
        src_dirs (list[str]): List of source directory relative path
        respect_git_ignore (bool): If True then function will return False if given directory is ignored by git
    Returns:
        src_dirs (list[os.PathLike]): List of Full path from `src_dirs`.
    '''
    src_dirs = filter(
        lambda x: x is not False,
        [get_src_dir_path(root_dir, src_dir, respect_git_ignore) for src_dir in src_dirs]
    )
    return set(src_dirs)

def get_src_dir_path(root_dir: os.PathLike, src_dir: str, respect_git_ignore: bool = True)-> bool | os.PathLike:
    '''method `get_src_dir_path`
    Args:
        root_dir (os.PathLike): base absolute path
        src_dir (str): source directory relative path
        respect_git_ignore (bool): If True then function will return False if given directory is ignored by git
    Returns:
        src_dir (bool | os.PathLike): False if path is ignored by git, Full `src_dir` path otherwise.
    '''
    src_dir = os.path.join(root_dir, src_dir)
    if not os.path.exists(src_dir) or (respect_git_ignore and is_ignored(src_dir)):
        return False
    return src_dir

def is_ignored(file_or_dir: str | os.PathLike) -> bool:
    '''Method `is_ignored`
    
    Args:
        file_or_dir (str): Name or path string of the file/directory to check
    
    Returns:
        is_ignored (bool): True if file/directory is ignore, false otherwise
        
    :raises:
        CalledProcessError: If return code for command `git check-ignore -q <file_or_dir>` not 0 or 1
    '''
    filepath = os.path.abspath(file_or_dir)
    try:
        check_call(f"git check-ignore -q {filepath}", shell=True)
    except CalledProcessError as cpe:
        if cpe.returncode != 1:
            logger = getLogger(__name__)
            logger.exception(f"failed to check is_ignored for filepath: {filepath}")
            raise cpe
        return False
    return True

__all__ = [
    "collect_files",
    "get_files",
    "pop_all",
    "get_src_dirs",
    "get_src_dir_path",
    "is_ignored"
]