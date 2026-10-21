"""课程门禁演示修复：恢复版本命令成功退出码的正确预期。"""
from buildchecker.cli import main


def test_version_returns_success_exit_code():
    """确认版本查询成功返回 0；此次仅修正测试预期，不改变实现。"""
    assert main(["version"]) == 0
