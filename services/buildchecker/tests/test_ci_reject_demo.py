"""课程门禁演示：先保存失败和拒绝合并证据，再修正错误预期。"""
from buildchecker.cli import main


def test_intentionally_wrong_version_exit_code():
    """故意把成功返回码写成 1，用于证明 CI 能阻止错误变更合并。"""
    assert main(["version"]) == 1, "门禁演示：version 实际成功返回 0"
