import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from importlib.util import find_spec
from pathlib import Path

import click
import tomllib
from honcho.manager import Manager as HonchoManager

from plain.runtime import APP_PATH, settings

from .db import cli as db_cli
from .pid import Pid
from .services import Services
from .utils import has_pyproject_toml, plainpackage_installed


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--port",
    "-p",
    default=8443,
    type=int,
    help="Port to run the web server on",
    envvar="PORT",
)
def cli(ctx, port):
    """Start local development"""

    if ctx.invoked_subcommand:
        return

    returncode = Dev(port=port).run()
    if returncode:
        sys.exit(returncode)


@cli.command()
def services():
    """Start additional services defined in pyproject.toml"""
    Services().run()


class Dev:
    def __init__(self, *, port):
        self.manager = HonchoManager()
        self.port = port
        self.plain_env = {
            **os.environ,
            "PYTHONUNBUFFERED": "true",
        }
        self.custom_process_env = {
            **self.plain_env,
            "PORT": str(self.port),
            "PYTHONPATH": os.path.join(APP_PATH.parent, "app"),
        }
        self.project_name = os.path.basename(os.getcwd())
        self.domain = f"{self.project_name}.localhost"

        # Paths for mkcert and certificates
        self.mkcert_dir = Path.home() / ".plain" / "dev"
        self.mkcert_bin = self.mkcert_dir / "mkcert"
        self.certs_dir = (
            Path(settings.PLAIN_TEMP_PATH) / "dev" / "certs"
        )  # Local project directory for certs

        # Define certificate and key paths with clear filenames
        self.cert_path = self.certs_dir / f"{self.domain}-cert.pem"
        self.key_path = self.certs_dir / f"{self.domain}-key.pem"

    def run(self):
        pid = Pid()
        pid.write()

        try:
            self.setup_mkcert()
            self.generate_certs()
            self.modify_hosts_file()
            self.add_csrf_trusted_origins()
            self.add_allowed_hosts()
            self.run_preflight()
            self.add_gunicorn()
            self.add_tailwind()
            self.add_pyproject_run()
            self.add_services()

            # Output the clickable link before starting the manager loop
            url = f"https://{self.domain}:{self.port}/"
            click.secho(
                f"\nYour application is running at: {click.style(url, fg='green', underline=True)}\n",
                bold=True,
            )

            self.manager.loop()

            return self.manager.returncode
        finally:
            pid.rm()

    def setup_mkcert(self):
        """Set up mkcert by checking if it's installed or downloading the binary and installing the local CA."""
        if mkcert_path := shutil.which("mkcert"):
            # mkcert is already installed somewhere
            self.mkcert_bin = mkcert_path
        else:
            self.mkcert_dir.mkdir(parents=True, exist_ok=True)
            if not self.mkcert_bin.exists():
                system = platform.system()
                arch = platform.machine()

                # Map platform.machine() to mkcert's expected architecture strings
                arch_map = {
                    "x86_64": "amd64",
                    "amd64": "amd64",
                    "AMD64": "amd64",
                    "arm64": "arm64",
                    "aarch64": "arm64",
                }
                arch = arch_map.get(
                    arch.lower(), "amd64"
                )  # Default to amd64 if unknown

                if system == "Darwin":
                    os_name = "darwin"
                elif system == "Linux":
                    os_name = "linux"
                elif system == "Windows":
                    os_name = "windows"
                else:
                    click.secho("Unsupported OS", fg="red")
                    sys.exit(1)

                mkcert_url = f"https://dl.filippo.io/mkcert/latest?for={os_name}/{arch}"
                click.secho(f"Downloading mkcert from {mkcert_url}...", bold=True)
                urllib.request.urlretrieve(mkcert_url, self.mkcert_bin)
                self.mkcert_bin.chmod(0o755)
            self.mkcert_bin = str(self.mkcert_bin)  # Convert Path object to string

        if not self.is_mkcert_ca_installed():
            click.secho(
                "Installing mkcert local CA. You may be prompted for your password.",
                bold=True,
            )
            subprocess.run([self.mkcert_bin, "-install"], check=True)

    def is_mkcert_ca_installed(self):
        """Check if mkcert local CA is already installed using mkcert -check."""
        try:
            result = subprocess.run([self.mkcert_bin, "-check"], capture_output=True)
            output = result.stdout.decode() + result.stderr.decode()
            if "The local CA is not installed" in output:
                return False
            return True
        except Exception as e:
            click.secho(f"Error checking mkcert CA installation: {e}", fg="red")
            return False

    def generate_certs(self):
        if self.cert_path.exists() and self.key_path.exists():
            return

        self.certs_dir.mkdir(parents=True, exist_ok=True)

        # Generate SSL certificates using mkcert
        click.secho(f"Generating SSL certificates for {self.domain}...", bold=True)
        subprocess.run(
            [
                self.mkcert_bin,
                "-cert-file",
                str(self.cert_path),
                "-key-file",
                str(self.key_path),
                self.domain,
            ],
            check=True,
        )

    def modify_hosts_file(self):
        """Modify the hosts file to map the custom domain to 127.0.0.1."""
        entry_identifier = "# Added by plain"
        hosts_entry = f"127.0.0.1 {self.domain}  {entry_identifier}"

        if platform.system() == "Windows":
            hosts_path = Path(r"C:\Windows\System32\drivers\etc\hosts")
            try:
                with hosts_path.open("r") as f:
                    content = f.read()

                if hosts_entry in content:
                    return  # Entry already exists; no action needed

                # Entry does not exist; add it
                with hosts_path.open("a") as f:
                    f.write(f"{hosts_entry}\n")
                click.secho(f"Added {self.domain} to {hosts_path}", bold=True)
            except PermissionError:
                click.secho(
                    "Permission denied while modifying hosts file. Please run the script as an administrator.",
                    fg="red",
                )
                sys.exit(1)
        else:
            # For macOS and Linux
            hosts_path = Path("/etc/hosts")
            try:
                with hosts_path.open("r") as f:
                    content = f.read()

                if hosts_entry in content:
                    return  # Entry already exists; no action needed

                # Entry does not exist; append it using sudo
                click.secho(
                    "Modifying /etc/hosts file. You may be prompted for your password.",
                    bold=True,
                )
                cmd = f"echo '{hosts_entry}' | sudo tee -a {hosts_path} >/dev/null"
                subprocess.run(cmd, shell=True, check=True)
                click.secho(f"Added {self.domain} to {hosts_path}", bold=True)
            except PermissionError:
                click.secho(
                    "Permission denied while accessing hosts file.",
                    fg="red",
                )
                sys.exit(1)
            except subprocess.CalledProcessError:
                click.secho(
                    "Failed to modify hosts file. Please ensure you have sudo privileges.",
                    fg="red",
                )
                sys.exit(1)

    def add_csrf_trusted_origins(self):
        csrf_trusted_origins = json.dumps(
            [
                f"https://{self.domain}:{self.port}",
            ]
        )

        click.secho(
            f"Automatically set PLAIN_CSRF_TRUSTED_ORIGINS={click.style(csrf_trusted_origins, underline=True)}",
            bold=True,
        )

        # Set environment variables
        self.plain_env["PLAIN_CSRF_TRUSTED_ORIGINS"] = csrf_trusted_origins
        self.custom_process_env["PLAIN_CSRF_TRUSTED_ORIGINS"] = csrf_trusted_origins

    def add_allowed_hosts(self):
        allowed_hosts = json.dumps([self.domain])

        click.secho(
            f"Automatically set PLAIN_ALLOWED_HOSTS={click.style(allowed_hosts, underline=True)}",
            bold=True,
        )

        # Set environment variables
        self.plain_env["PLAIN_ALLOWED_HOSTS"] = allowed_hosts
        self.custom_process_env["PLAIN_ALLOWED_HOSTS"] = allowed_hosts

    def run_preflight(self):
        if subprocess.run(["plain", "preflight"], env=self.plain_env).returncode:
            click.secho("Preflight check failed!", fg="red")
            sys.exit(1)

    def add_gunicorn(self):
        plain_db_installed = find_spec("plain.models") is not None

        # Watch .env files for reload
        extra_watch_files = []
        for f in os.listdir(APP_PATH.parent):
            if f.startswith(".env"):
                extra_watch_files.append(f)

        reload_extra = " ".join(f"--reload-extra-file {f}" for f in extra_watch_files)
        gunicorn_cmd = [
            "gunicorn",
            "--bind",
            f"{self.domain}:{self.port}",
            "--certfile",
            str(self.cert_path),
            "--keyfile",
            str(self.key_path),
            "--reload",
            "plain.wsgi:app",
            "--timeout",
            "60",
            "--access-logfile",
            "-",
            "--error-logfile",
            "-",
            *reload_extra.split(),
            "--access-logformat",
            "'\"%(r)s\" status=%(s)s length=%(b)s dur=%(M)sms'",
        ]
        gunicorn = " ".join(gunicorn_cmd)

        if plain_db_installed:
            runserver_cmd = f"plain models db-wait && plain migrate && {gunicorn}"
        else:
            runserver_cmd = gunicorn

        if "WEB_CONCURRENCY" not in self.plain_env:
            # Default to two workers to prevent lockups
            self.plain_env["WEB_CONCURRENCY"] = "2"

        self.manager.add_process("plain", runserver_cmd, env=self.plain_env)

    def add_tailwind(self):
        if not plainpackage_installed("tailwind"):
            return

        self.manager.add_process("tailwind", "plain tailwind compile --watch")

    def add_pyproject_run(self):
        if not has_pyproject_toml(APP_PATH.parent):
            return

        with open(Path(APP_PATH.parent, "pyproject.toml"), "rb") as f:
            pyproject = tomllib.load(f)

        run_commands = (
            pyproject.get("tool", {}).get("plain", {}).get("dev", {}).get("run", {})
        )
        for name, data in run_commands.items():
            env = {
                **self.custom_process_env,
                **data.get("env", {}),
            }
            self.manager.add_process(name, data["cmd"], env=env)

    def add_services(self):
        services = Services.get_services(APP_PATH.parent)
        for name, data in services.items():
            env = {
                **os.environ,
                "PYTHONUNBUFFERED": "true",
                **data.get("env", {}),
            }
            self.manager.add_process(name, data["cmd"], env=env)


cli.add_command(db_cli)
