from types import FrameType
import coverage


class BismuthCoverage(coverage.CoveragePlugin):
    def dynamic_context(self, frame: FrameType):
        co_name = frame.f_code.co_name
        if co_name.startswith("test") or co_name == "runTest":
            return f"{frame.f_code.co_filename}:{frame.f_code.co_firstlineno}"


def coverage_init(reg, _options):
    reg.add_dynamic_context(BismuthCoverage())
