import rich_click as click
import subprocess
import sys
from novara.utils import logger, SSHKEY_FILE
from novara.config import config


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.pass_context
def docker(ctx):
    """this command allows you to control the docker on the remote with the docker cli"""

    docker = subprocess.Popen(["ssh", "-i", SSHKEY_FILE, f"{config.ssh_user}@{config.ssh_url}", "-p", f"{config.ssh_port}", "docker", *ctx.args], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    try:
        docker.wait()
    except KeyboardInterrupt:
        logger.warning("terminating cli")
    docker.kill()
