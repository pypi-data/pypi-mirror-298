from typing import List, Tuple, Optional
from malevich_app.docker_export.pipeline import run_processor, run_output, run_condition
from malevich_app.export.abstract.abstract import Collection
from malevich_app.export.jls.df import JDF
from malevich_app.export.secondary.helpers import call_async_fun
from malevich_app.export.secondary.logger import output_logger, processor_logger, condition_logger


class JuliusPipelineItem:
    def __init__(self, japp):
        self.japp = japp

    async def run_processor(self, dfs: List[JDF]) -> Tuple[bool, Optional[List[Collection]]]:
        ok, colls = await call_async_fun(lambda: run_processor(self.japp, dfs, processor_logger), processor_logger, self.japp.debug_mode, self.japp.logs_buffer, on_error=(False, None))    # colls - None or List[Tuple[Collection, ...]]
        if ok:
            # FIXME difference between error in code & internal error, ignore user errors
            ok, colls = await call_async_fun(lambda: run_output(self.japp, colls, output_logger), output_logger, self.japp.debug_mode, self.japp.logs_buffer, on_error=(False, None))       # colls - List[Collection]
        return ok, colls

    async def run_condition(self, dfs: List[JDF]) -> Tuple[bool, bool]:
        return await call_async_fun(lambda: run_condition(self.japp, dfs, condition_logger), condition_logger, self.japp.debug_mode, self.japp.logs_buffer, on_error=(False, False))
