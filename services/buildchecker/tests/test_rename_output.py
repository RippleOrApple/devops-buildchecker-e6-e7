"""验证临时产物重命名后仍能正确归属最终构建目标。"""
from pathlib import PurePosixPath

from buildchecker.fullcheck import execution_graph


def test_renamed_output_keeps_inputs_and_excludes_temporary_file(tmp_path):
    """确认 rename 后保留真实输入，并排除任务自身生成的临时文件。"""
    project_root = PurePosixPath("/", tmp_path.name).as_posix()
    traces = {
        "t.10": (
            'execve("make", ["make", "app"], []) = 0\n'
            'clone(child_stack=NULL, flags=SIGCHLD) = 11\n'
        ),
        "t.11": (
            'execve("cc", ["cc", "-c", "unit.c"], []) = 0\n'
            'openat(AT_FDCWD, "unit.c", O_RDONLY) = 3\n'
            'openat(AT_FDCWD, "needed.h", O_RDONLY) = 4\n'
            'openat(AT_FDCWD, "unit.tmp", O_WRONLY|O_CREAT, 0666) = 5\n'
            'openat(AT_FDCWD, "unit.tmp", O_RDONLY) = 6\n'
            'rename("unit.tmp", "unit.o") = 0\n'
        ),
    }
    for name, content in traces.items():
        (tmp_path / name).write_text(content, encoding="utf-8")

    targets, _ = execution_graph(tmp_path, project_root)

    assert set(targets) == {"unit.o"}
    assert set(targets["unit.o"]["dependencies"]) == {"unit.c", "needed.h"}
    assert targets["unit.o"]["job_pid"] == 11
    assert targets["unit.o"]["output_evidence"] == {
        "source": "system_call",
        "trace_file": "t.11",
        "line": 6,
        "pid": 11,
        "operation": "rename",
    }
