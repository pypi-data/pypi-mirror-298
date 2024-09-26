import logging
import os
import pathlib
import traceback
import uuid
from typing import Optional, Union, Dict, Any, Callable
from malevich_app.export.abstract.abstract import InitPipeline, InitRun, RunPipeline, FunMetadata, AppFunctionsInfo, LocalRunStruct, Image, PipelineStructureUpdate, Cfg
from malevich_app.export.abstract.pipeline import Pipeline
from malevich_app.export.jls.JuliusPipeline import JuliusPipeline
from malevich_app.export.jls.JuliusRegistry import JuliusRegistry
from malevich_app.export.jls.LocalLogsBuffer import LocalLogsBuffer
from malevich_app.export.secondary.State import states, State
from malevich_app.local.LocalStorage import LocalStorage
from malevich_app.local.log import base_logger_fun
from malevich_app.local.utils import init_settings, scheme_class_columns, fix_cfg


class LocalRunner:
    def __init__(self, local_settings: LocalRunStruct, logger_fun: Optional[Callable[[str, Optional[str], Optional[str], bool], logging.Logger]] = None):
        init_settings(local_settings)

        self.__logger_fun = logger_fun if logger_fun is not None else base_logger_fun
        self.__registry = JuliusRegistry(local_settings.import_dirs, logger_fun=self.__logger_fun)
        self.__storage: LocalStorage = LocalStorage(local_settings, {k: scheme_class_columns(v) for k, v in self.__registry.schemes().items()})
        self.__registry._set_local_storage(self.__storage)
        self.__local_settings = local_settings
        self.__secret = str(uuid.uuid4())   # FIXME one secret for operation_id

    @property
    def app_info(self) -> AppFunctionsInfo:
        with open(os.path.join(pathlib.Path(__file__).parent.parent.resolve(), "version"), 'r') as f:
            version = f.readline()
        try:
            self.__registry.info.version = version
            return self.__registry.info
        except:
            return AppFunctionsInfo(logs=traceback.format_exc(), version=version)

    @property
    def storage(self) -> LocalStorage:
        return self.__storage

    async def __init(self, init: InitPipeline):
        state = states.get(init.operationId)
        assert state is None, f"pipeline already inited, operationId {init.operationId}"

        try:
            state = State(init.operationId, init.schemesNames, init.scale, logs_buffer=LocalLogsBuffer(self.__logger_fun, init.operationId))
            states[init.operationId] = state
            j_pipeline = JuliusPipeline(init, self.__registry, state.logs_buffer, storage=self.__storage)
            state.pipeline = j_pipeline
            state.schemes_names.update(j_pipeline.scheme_aliases())
            j_pipeline.set_exist_schemes(None, state.schemes_names)

            await self.__registry.update_schemes_pipeline(init.operationId)
        except BaseException as ex:
            if state is not None:
                state.logs_buffer.write(f"{traceback.format_exc()}\n")
            states.pop(init.operationId, None)
            raise Exception("init pipeline failed") from ex

        if not await j_pipeline.init():
            states.pop(init.operationId, None)
            raise Exception("init failed")

        self.__registry.save_schemes(init.operationId)  # TODO not need local?

    async def __init_run(self, init: InitRun):
        state = states.get(init.operationId)
        assert state is not None, f"wrong operationId {init.operationId}"

        if state.pipeline is None:
            state.logs_buffer.write("error: init_run pipeline failed before, can't run\n")
        try:
            res = await state.pipeline.init_run(init)
            assert res, "not init"
            state.pipeline.set_exist_schemes(init.runId, state.schemes_names)
        except BaseException as ex:
            raise Exception("init_run failed") from ex

    async def __run(self, run: RunPipeline):
        state = states.get(run.operationId)
        assert state is not None, f"wrong operationId {run.operationId}"

        if not state.pipeline.exist_run(run.runId):
            state.logs_buffer.write(f"/run/pipeline wrong runId {run.runId}\n")
            raise Exception(f"runId {run.runId} already exist")

        state.pipeline.set_index(run.runId, run.index)  # TODO check that it work
        try:
            ok = await state.pipeline.run(run.runId, run.iteration, run.bindId, run.data, run.conditions, run.structureUpdate, run.bindIdsDependencies)
        except BaseException as ex:
            state.logs_buffer.write(traceback.format_exc())
            raise Exception("run failed") from ex
        if not ok:
            raise Exception("run failed")

    async def __finish(self, metadata: FunMetadata):
        state = states.get(metadata.operationId)
        assert state is not None, f"finish wrong operationId {metadata.operationId}"
        if metadata.runId is None:
            states.pop(metadata.operationId)
        else:
            state.pipeline.delete_run(metadata.runId)

    async def prepare(self, pipeline: Pipeline, cfg: Optional[Union[Dict[str, Any], str, Cfg]] = None, debug_mode: bool = False, profile_mode: Optional[str] = None) -> str:
        if cfg is not None:
            cfg = fix_cfg(cfg)

        operation_id = str(uuid.uuid4())

        pipeline = InitPipeline(
            cfg=cfg,
            infoUrl=None,
            debugMode=debug_mode,
            profileMode=profile_mode,
            operationId=operation_id,
            dagHost="",     # TODO ok?

            login=self.__local_settings.login,
            pipeline=pipeline,
            schemesNames=[],
            image=Image(ref=""),
            scale=1,
            processorIds=set(pipeline.processors.keys()),
            secret=self.__secret,
            singlePod=True,
            continueAfterProcessor=False,
        )
        await self.__init(pipeline)
        return operation_id

    async def run(self, operation_id: str, run_id: str, cfg: Optional[Union[Dict[str, Any], str, Cfg]] = None, debug_mode: bool = False, profile_mode: Optional[str] = None):
        if cfg is not None:
            cfg = fix_cfg(cfg)

        init = InitRun(
            cfg=cfg,
            infoUrl=None,
            debugMode=debug_mode,
            profileMode=profile_mode,
            operationId=operation_id,
            dagHost="",

            runId=run_id,
            kafkaInitRun=None,
        )
        await self.__init_run(init)
        run = RunPipeline(
            runId=run_id,
            operationId=operation_id,

            iteration=0,
            bindId="",  # not matter
            data=None,
            conditions=None,
            index=0,
            structureUpdate=PipelineStructureUpdate(),
            bindIdsDependencies=None,
        )
        await self.__run(run)

    async def stop(self, operation_id: str, run_id: Optional[str] = None):
        metadata = FunMetadata(
            runId=run_id,
            operationId=operation_id,
        )
        await self.__finish(metadata)

    async def run_full(self, pipeline: Pipeline, cfg: Optional[Union[Dict[str, Any], str, Cfg]] = None, debug_mode: bool = False, profile_mode: Optional[str] = None) -> str:
        if cfg is not None:
            cfg = fix_cfg(cfg)

        operation_id = await self.prepare(pipeline, None, debug_mode, profile_mode)
        run_id = ""
        await self.run(operation_id, run_id, cfg, debug_mode, profile_mode)
        await self.stop(operation_id, run_id)
        return operation_id
