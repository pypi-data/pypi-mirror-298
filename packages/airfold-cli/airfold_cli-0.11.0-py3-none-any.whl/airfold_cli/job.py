from typing import Annotated

from typer import Argument, Context

from airfold_cli import app
from airfold_cli.api import AirfoldApi
from airfold_cli.cli import AirfoldTyper
from airfold_cli.completion import cancel_job_ids_completion
from airfold_cli.models import PipeInfo
from airfold_cli.options import WaitOption, with_global_options
from airfold_cli.root import catch_airfold_error
from airfold_cli.utils import dump_json

job_app = AirfoldTyper(
    name="job",
    help="Job commands.",
)

app.add_typer(job_app)


@job_app.command("ls")
@catch_airfold_error()
@with_global_options
def ls(ctx: Context) -> None:
    """List jobs.
    \f

    Args:
        ctx: Typer context

    """
    job_app.apply_options(ctx)

    api = AirfoldApi.from_config()

    jobs_info: list[PipeInfo] = api.list_jobs()

    if not jobs_info:
        if job_app.is_terminal():
            job_app.console.print("\t[magenta]NO JOBS[/magenta]")
        return

    data: list[dict] = [job_info.dict(humanize=True) for job_info in jobs_info]
    if job_app.is_terminal():
        columns = {
            "Id": "name",
            "Status": "status",
            "Created": "created",
            "Updated": "updated",
            "Data": "data",
        }
        job_app.ui.print_table(columns, data=data, title=f"{len(jobs_info)} jobs")
    else:
        for job_info in jobs_info:
            job_app.console.print(dump_json(job_info.dict()))


@job_app.command("cancel")
@catch_airfold_error()
@with_global_options
def cancel(
    ctx: Context,
    job_id: Annotated[str, Argument(help="Job ID.", autocompletion=cancel_job_ids_completion)],
    wait: Annotated[bool, WaitOption] = False,
) -> None:
    """Cancel job.
    \f

    Args:
        ctx: Typer context
        job_id: Job ID
        wait: Wait for job cancellation to complete
    """
    job_app.apply_options(ctx)

    api = AirfoldApi.from_config()

    api.cancel_job(job_id, wait=wait)

    if job_app.is_terminal():
        job_app.ui.print_success(f"Job [cyan]'{job_id}'[/cyan] canceled")
