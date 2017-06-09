"""
base_utils: utilities that does not need app_config instance
"""
import os
import logging
import itertools
import fcntl

from contextlib import contextmanager

logger = logging.getLogger(__name__)

def firstline(lines):
    lines = lines or ''
    lines = lines.strip().splitlines()
    if not lines: return ''
    return lines[0].strip()


def try_int(i, fallback=None):
    try: return int(i)
    except ValueError: pass
    except TypeError: pass
    return fallback

def try_float(i, fallback=None):
    try: return int(i)
    except ValueError: pass
    except TypeError: pass
    return fallback

def safe_base64(txt):
    return txt.encode('base64').strip(' \n\r\t=').replace('/', '-').replace('+', '_')

def resolve_dotted_name(name):
    """Return object referenced by dotted name.
    :param name: dotted name as a String.
    :return: Resolved Python object.
    :raises ImportError: If can't resolve ``nane``
    Examples:
        >>> resolve_dotted_name('sys.exit')
        <built-in function exit>
        >>> resolve_dotted_name('xml.etree.ElementTree')  # doctest: +ELLIPSIS
        <module 'xml.etree.ElementTree' ...>
        >>> resolve_dotted_name('distconfig.backends.zookeeper.ZooKeeperBackend')
        <class 'distconfig.backends.zookeeper.ZooKeeperBackend'>
    """
    paths = name.split('.')
    current = paths[0]
    found = __import__(current)
    for part in paths[1:]:
        current += '.' + part
        try:
            found = getattr(found, part)
        except AttributeError:
            found = __import__(current, fromlist=part)
    return found


def assert_dirs(dest_dir):
    try: os.makedirs(dest_dir)
    except OSError:
        if not os.path.isdir(dest_dir):
            logger.error("cloud not create directories=[%r]", dest_dir)
            raise

def assert_file_dirs(filename):
    dest_dir = os.path.dirname(filename)
    try: os.makedirs(dest_dir)
    except OSError:
        if not os.path.isdir(dest_dir):
            logger.error("cloud not create directories=[%r]", dest_dir)
            raise


def factory(dotted_name, *args, **kw):
    """
    pass `dotted_name` to `resolve_dotted_name` then call it passing the rest of arguments
    """
    return resolve_dotted_name(dotted_name)(*args, **kw)



@contextmanager
def file_lock(fd, lock_type=fcntl.LOCK_EX):
    """
    Locks FD before entering the context, always releasing the lock.
    """
    try:
        fcntl.flock(fd, lock_type)
        yield fd
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)

def get_chunks(chunk_size, items):
    """
    split an iteratable object into fixed-sized chunks
    """
    it = iter(items)
    while True:
        chunk0 = tuple(itertools.islice(it, chunk_size))
        if not chunk0: break
        yield chunk0
