import re
from loguru import logger
import loguru._recattrs as recattrs


def test_patch_record_file(writer):
    def patch(record):
        record["file"].name = "456"
        record["file"].path = "123/456"

    logger.add(writer, format="{file} {file.name} {file.path}")
    logger.patch(patch).info("Test")

    assert writer.read() == "456 456 123/456\n"


def test_patch_record_thread(writer):
    def patch(record):
        record["thread"].id = 111
        record["thread"].name = "Thread-111"

    logger.add(writer, format="{thread} {thread.name} {thread.id}")
    logger.patch(patch).info("Test")

    assert writer.read() == "111 Thread-111 111\n"


def test_patch_record_process(writer):
    def patch(record):
        record["process"].id = 123
        record["process"].name = "Process-123"

    logger.add(writer, format="{process} {process.name} {process.id}")
    logger.patch(patch).info("Test")

    assert writer.read() == "123 Process-123 123\n"


def test_level_repr():
    level = recattrs.LevelRecattr("FOO", 123, "!!")
    assert repr(level) == "(name='FOO', no=123, icon='!!')"


def test_file_repr():
    file_ = recattrs.FileRecattr("foo.txt", "path/foo.txt")
    assert repr(file_) == "(name='foo.txt', path='path/foo.txt')"


def test_thread_repr():
    thread = recattrs.ThreadRecattr(98765, "thread-1")
    assert repr(thread) == "(id=98765, name='thread-1')"


def test_process_repr():
    process = recattrs.ProcessRecattr(12345, "process-1")
    assert repr(process) == "(id=12345, name='process-1')"


def test_exception_repr():
    exception = recattrs.ExceptionRecattr(ValueError, ValueError("Nope"), None)
    regex = r"\(type=<class 'ValueError'>, value=ValueError\('Nope',?\), traceback=None\)"
    assert re.fullmatch(regex, repr(exception))
