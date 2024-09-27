import bugsnag
from bugsnag_client import (
    add_batch_metadata as bugsnag_add_batch_metadata,
    remove_nix_hash as bugsnag_remove_nix_hash,
)
from fluid_sbom.context import (
    BASE_DIR,
    CI_COMMIT_SHORT_SHA,
)
from fluid_sbom.utils.env import (
    guess_environment,
)
import logging


def initialize_bugsnag() -> None:
    bugsnag.before_notify(bugsnag_add_batch_metadata)
    bugsnag.before_notify(bugsnag_remove_nix_hash)
    bugsnag.configure(
        ignore_classes=["SystemExit"],
        breadcrumb_log_level=logging.DEBUG,
        notify_release_stages=["production"],
        release_stage=guess_environment(),
        app_version=CI_COMMIT_SHORT_SHA,
        project_root=BASE_DIR,
    )
    bugsnag.start_session()
