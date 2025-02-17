from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union
from vllm.worker.worker_base import WorkerWrapperBase
from vllm.utils import (enable_trace_function_call_for_thread,
                        resolve_obj_by_qualname, update_environment_variables)
from vllm.config import set_current_vllm_config
from molink.worker.worker import MolinkWorker

class MolinkWorkerWrapperBase(WorkerWrapperBase):


    def init_worker(self, all_kwargs: List[Dict[str, Any]]) -> None:
        """
        Here we inject some common logic before initializing the worker.
        Arguments are passed to the worker class constructor.
        """
        kwargs = all_kwargs[self.rpc_rank]
        self.vllm_config = kwargs.get("vllm_config", None)
        assert self.vllm_config is not None, (
            "vllm_config is required to initialize the worker")
        enable_trace_function_call_for_thread(self.vllm_config)

        from vllm.plugins import load_general_plugins
        load_general_plugins()

        print('*' * 200)
        print(kwargs)
        with set_current_vllm_config(self.vllm_config):
            # To make vLLM config available during worker initialization
            self.worker = MolinkWorker(**kwargs)
            assert self.worker is not None
