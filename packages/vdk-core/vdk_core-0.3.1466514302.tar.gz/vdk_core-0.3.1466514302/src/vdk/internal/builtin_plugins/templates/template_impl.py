# Copyright 2023-2024 Broadcom
# SPDX-License-Identifier: Apache-2.0
import copy
import logging
import pathlib
from typing import Dict
from typing import Optional

from vdk.api.job_input import ITemplate
from vdk.api.plugin.plugin_input import ITemplateRegistry
from vdk.internal.builtin_plugins.run.data_job import DataJobFactory
from vdk.internal.builtin_plugins.run.execution_results import ExecutionResult
from vdk.internal.core import errors
from vdk.internal.core.context import CoreContext

log = logging.getLogger(__name__)


class TemplatesImpl(ITemplateRegistry, ITemplate):
    def __init__(
        self,
        job_name: str,
        core_context: CoreContext,
        datajob_factory: DataJobFactory = None,
        template_name: Optional[str] = None,
    ):
        self._job_name = job_name
        self._core_context = core_context
        self._registered_templates: Dict[str, Dict[str, pathlib.Path]] = {}
        self._datajob_factory = (
            DataJobFactory() if datajob_factory is None else datajob_factory
        )
        self._template_name = template_name

    def add_template(
        self, name: str, template_directory: pathlib.Path, database: str = "default"
    ):
        if (
            database in self._registered_templates
            and name in self._registered_templates[database]
            and self._registered_templates[database][name] != template_directory
        ):
            log.warning(
                f"Template with name {name} in database {database} has been registered with directory "
                f"{self._registered_templates[database][name]}."
                f"We will overwrite it with new directory {template_directory} now."
            )
        if database not in self._registered_templates:
            self._registered_templates[database] = {}
        self._registered_templates[database][name] = template_directory

    # Added database argument to support multiple DB type
    def execute_template(
        self, name: str, template_args: dict, database: str = "default"
    ) -> ExecutionResult:  # input dict immutable?
        log.info(f"Execute template {database} {name} {template_args}")
        template_directory = self.get_template_directory(name, database)
        if database != "default":
            core_context = CoreContext(
                self._core_context.plugin_registry,
                copy.deepcopy(self._core_context.configuration),
                self._core_context.state.clone(),
            )
            core_context.configuration.override_value(
                "DB_DEFAULT_TYPE", database, "vdk"
            )
            template_job = self._datajob_factory.new_datajob(
                template_directory, core_context, name=self._job_name
            )
        else:
            template_job = self._datajob_factory.new_datajob(
                template_directory, self._core_context, name=self._job_name
            )

        result = template_job.run(template_args, name)
        if result.is_failed():
            if result.get_exception_to_raise():
                raise result.get_exception_to_raise()
            else:
                errors.report_and_throw(
                    errors.PlatformServiceError(
                        f"Template `{name}` failed.",
                        f"No exception is reported. This is not expected. "
                        f"Execution steps of templates were {result.steps_list}",
                        "We will raise an exception now. Likely the job will fail.",
                        f"Check out the error and fix the template invocation "
                        f"or fix the template by installing the correct plugin."
                        f" Or open an issue on the support team or "
                        f"Versatile Data Kit or the plugin provider of the template",
                    )
                )
        return result

    def get_template_directory(
        self, name: str, database: str = "default"
    ) -> pathlib.Path:
        if (
            database in self._registered_templates
            and name in self._registered_templates[database]
        ):
            return self._registered_templates[database][name]
        else:
            errors.report_and_throw(
                errors.UserCodeError(
                    f"No registered template with name: {name} and database {database}.",
                    "Template with that name has not been registered",
                    "Make sure you have not misspelled the name of the template "
                    "or the plugin(s) providing the template is installed. "
                    f"Current list of templated is: {list(self._registered_templates.keys())}",
                )
            )
