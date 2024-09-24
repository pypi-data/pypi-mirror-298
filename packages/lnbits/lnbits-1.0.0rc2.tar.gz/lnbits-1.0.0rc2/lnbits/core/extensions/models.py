from __future__ import annotations

import asyncio
import hashlib
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any, NamedTuple, Optional

import httpx
from loguru import logger
from pydantic import BaseModel

from lnbits.settings import settings

from .helpers import (
    download_url,
    file_hash,
    github_api_get,
    icon_to_github_url,
    version_parse,
)


class ExplicitRelease(BaseModel):
    id: str
    name: str
    version: str
    archive: str
    hash: str
    dependencies: list[str] = []
    repo: Optional[str]
    icon: Optional[str]
    short_description: Optional[str]
    min_lnbits_version: Optional[str]
    html_url: Optional[str]  # todo: release_url
    warning: Optional[str]
    info_notification: Optional[str]
    critical_notification: Optional[str]
    details_link: Optional[str]
    pay_link: Optional[str]

    def is_version_compatible(self):
        if not self.min_lnbits_version:
            return True
        return version_parse(self.min_lnbits_version) <= version_parse(settings.version)


class GitHubRelease(BaseModel):
    id: str
    organisation: str
    repository: str


class Manifest(BaseModel):
    featured: list[str] = []
    extensions: list[ExplicitRelease] = []
    repos: list[GitHubRelease] = []


class GitHubRepoRelease(BaseModel):
    name: str
    tag_name: str
    zipball_url: str
    html_url: str

    def details_link(self, source_repo: str) -> str:
        return f"https://raw.githubusercontent.com/{source_repo}/{self.tag_name}/config.json"


class GitHubRepo(BaseModel):
    stargazers_count: str
    html_url: str
    default_branch: str


class ExtensionConfig(BaseModel):
    name: str
    short_description: str
    tile: str = ""
    warning: Optional[str] = ""
    min_lnbits_version: Optional[str]

    def is_version_compatible(self):
        if not self.min_lnbits_version:
            return True
        return version_parse(self.min_lnbits_version) <= version_parse(settings.version)

    @classmethod
    async def fetch_github_release_config(
        cls, org: str, repo: str, tag_name: str
    ) -> Optional[ExtensionConfig]:
        config_url = (
            f"https://raw.githubusercontent.com/{org}/{repo}/{tag_name}/config.json"
        )
        error_msg = "Cannot fetch GitHub extension config"
        config = await github_api_get(config_url, error_msg)
        return ExtensionConfig.parse_obj(config)


class ReleasePaymentInfo(BaseModel):
    amount: Optional[int] = None
    pay_link: Optional[str] = None
    payment_hash: Optional[str] = None
    payment_request: Optional[str] = None


class PayToEnableInfo(BaseModel):
    required: Optional[bool] = False
    amount: Optional[int] = None
    wallet: Optional[str] = None


class UserExtensionInfo(BaseModel):
    paid_to_enable: Optional[bool] = False
    payment_hash_to_enable: Optional[str] = None


class UserExtension(BaseModel):
    extension: str
    active: bool
    extra: Optional[UserExtensionInfo] = None

    @property
    def is_paid(self) -> bool:
        if not self.extra:
            return False
        return self.extra.paid_to_enable is True

    @classmethod
    def from_row(cls, data: dict) -> UserExtension:
        ext = UserExtension(**data)
        ext.extra = (
            UserExtensionInfo(**json.loads(data["_extra"] or "{}"))
            if "_extra" in data
            else None
        )
        return ext


class Extension(NamedTuple):
    code: str
    is_valid: bool
    is_admin_only: bool
    name: Optional[str] = None
    short_description: Optional[str] = None
    tile: Optional[str] = None
    contributors: Optional[list[str]] = None
    hidden: bool = False
    migration_module: Optional[str] = None
    db_name: Optional[str] = None
    upgrade_hash: Optional[str] = ""

    @property
    def module_name(self) -> str:
        if self.is_upgrade_extension:
            if settings.has_default_extension_path:
                return f"lnbits.upgrades.{self.code}-{self.upgrade_hash}"
            return f"{self.code}-{self.upgrade_hash}"

        if settings.has_default_extension_path:
            return f"lnbits.extensions.{self.code}"
        return self.code

    @property
    def is_upgrade_extension(self) -> bool:
        return self.upgrade_hash != ""

    @classmethod
    def from_installable_ext(cls, ext_info: InstallableExtension) -> Extension:
        return Extension(
            code=ext_info.id,
            is_valid=True,
            is_admin_only=False,  # todo: is admin only
            name=ext_info.name,
            upgrade_hash=ext_info.hash if ext_info.module_installed else "",
        )

    @classmethod
    def get_valid_extensions(
        cls, include_deactivated: Optional[bool] = True
    ) -> list[Extension]:
        valid_extensions = [
            extension for extension in cls._extensions() if extension.is_valid
        ]

        if include_deactivated:
            return valid_extensions

        if settings.lnbits_extensions_deactivate_all:
            return []

        return [
            e
            for e in valid_extensions
            if e.code not in settings.lnbits_deactivated_extensions
        ]

    @classmethod
    def get_valid_extension(
        cls, ext_id: str, include_deactivated: Optional[bool] = True
    ) -> Optional[Extension]:
        all_extensions = cls.get_valid_extensions(include_deactivated)
        return next((e for e in all_extensions if e.code == ext_id), None)

    @classmethod
    def _extensions(cls) -> list[Extension]:
        p = Path(settings.lnbits_extensions_path, "extensions")
        Path(p).mkdir(parents=True, exist_ok=True)
        extension_folders: list[Path] = [f for f in p.iterdir() if f.is_dir()]

        # todo: remove this property somehow, it is too expensive
        output: list[Extension] = []

        for extension_folder in extension_folders:
            extension_code = extension_folder.parts[-1]
            try:
                with open(extension_folder / "config.json") as json_file:
                    config = json.load(json_file)
                is_valid = True
                is_admin_only = extension_code in settings.lnbits_admin_extensions
            except Exception:
                config = {}
                is_valid = False
                is_admin_only = False

            output.append(
                Extension(
                    extension_code,
                    is_valid,
                    is_admin_only,
                    config.get("name"),
                    config.get("short_description"),
                    config.get("tile"),
                    config.get("contributors"),
                    config.get("hidden") or False,
                    config.get("migration_module"),
                    config.get("db_name"),
                )
            )

        return output


class ExtensionRelease(BaseModel):
    name: str
    version: str
    archive: str
    source_repo: str
    is_github_release: bool = False
    hash: Optional[str] = None
    min_lnbits_version: Optional[str] = None
    is_version_compatible: Optional[bool] = True
    html_url: Optional[str] = None
    description: Optional[str] = None
    warning: Optional[str] = None
    repo: Optional[str] = None
    icon: Optional[str] = None
    details_link: Optional[str] = None

    pay_link: Optional[str] = None
    cost_sats: Optional[int] = None
    paid_sats: Optional[int] = 0
    payment_hash: Optional[str] = None

    @property
    def archive_url(self) -> str:
        if not self.pay_link:
            return self.archive
        return (
            f"{self.archive}?version=v{self.version}&payment_hash={self.payment_hash}"
        )

    async def check_payment_requirements(self):
        if not self.pay_link:
            return

        payment_info = await self.fetch_release_payment_info()
        self.cost_sats = payment_info.amount if payment_info else None

    async def fetch_release_payment_info(
        self, amount: Optional[int] = None
    ) -> Optional[ReleasePaymentInfo]:
        url = f"{self.pay_link}?amount={amount}" if amount else self.pay_link
        assert url, "Missing URL for payment info."
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                resp.raise_for_status()
                return ReleasePaymentInfo(**resp.json())
        except Exception as e:
            logger.warning(e)
            return None

    @classmethod
    def from_github_release(
        cls, source_repo: str, r: GitHubRepoRelease
    ) -> ExtensionRelease:
        return ExtensionRelease(
            name=r.name,
            description=r.name,
            version=r.tag_name,
            archive=r.zipball_url,
            source_repo=source_repo,
            is_github_release=True,
            details_link=r.details_link(source_repo),
            repo=f"https://github.com/{source_repo}",
            html_url=r.html_url,
        )

    @classmethod
    def from_explicit_release(
        cls, source_repo: str, e: ExplicitRelease
    ) -> ExtensionRelease:
        return ExtensionRelease(
            name=e.name,
            version=e.version,
            archive=e.archive,
            hash=e.hash,
            source_repo=source_repo,
            description=e.short_description,
            min_lnbits_version=e.min_lnbits_version,
            is_version_compatible=e.is_version_compatible(),
            warning=e.warning,
            html_url=e.html_url,
            details_link=e.details_link,
            pay_link=e.pay_link,
            repo=e.repo,
            icon=e.icon,
        )

    @classmethod
    async def get_github_releases(cls, org: str, repo: str) -> list[ExtensionRelease]:
        try:
            github_releases = await cls.fetch_github_releases(org, repo)
            return [
                ExtensionRelease.from_github_release(f"{org}/{repo}", r)
                for r in github_releases
            ]
        except Exception as e:
            logger.warning(e)
            return []

    @classmethod
    async def fetch_github_releases(
        cls, org: str, repo: str
    ) -> list[GitHubRepoRelease]:
        releases_url = f"https://api.github.com/repos/{org}/{repo}/releases"
        error_msg = "Cannot fetch extension releases"
        releases = await github_api_get(releases_url, error_msg)
        return [GitHubRepoRelease.parse_obj(r) for r in releases]

    @classmethod
    async def fetch_release_details(cls, details_link: str) -> Optional[dict]:

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(details_link)
                resp.raise_for_status()
                data = resp.json()
                if "description_md" in data:
                    resp = await client.get(data["description_md"])
                    if not resp.is_error:
                        data["description_md"] = resp.text

                return data
        except Exception as e:
            logger.warning(e)
            return None


class InstallableExtension(BaseModel):
    id: str
    name: str
    active: Optional[bool] = False
    short_description: Optional[str] = None
    icon: Optional[str] = None
    dependencies: list[str] = []
    is_admin_only: bool = False
    stars: int = 0
    featured = False
    latest_release: Optional[ExtensionRelease] = None
    installed_release: Optional[ExtensionRelease] = None
    payments: list[ReleasePaymentInfo] = []
    pay_to_enable: Optional[PayToEnableInfo] = None
    archive: Optional[str] = None

    @property
    def hash(self) -> str:
        if self.installed_release:
            if self.installed_release.hash:
                return self.installed_release.hash
            m = hashlib.sha256()
            m.update(f"{self.installed_release.archive}".encode())
            return m.hexdigest()
        return "not-installed"

    @property
    def zip_path(self) -> Path:
        extensions_data_dir = Path(settings.lnbits_data_folder, "zips")
        Path(extensions_data_dir).mkdir(parents=True, exist_ok=True)
        return Path(extensions_data_dir, f"{self.id}.zip")

    @property
    def ext_dir(self) -> Path:
        return Path(settings.lnbits_extensions_path, "extensions", self.id)

    @property
    def ext_upgrade_dir(self) -> Path:
        return Path(
            settings.lnbits_extensions_path, "upgrades", f"{self.id}-{self.hash}"
        )

    @property
    def module_name(self) -> str:
        if settings.has_default_extension_path:
            return f"lnbits.extensions.{self.id}"
        return self.id

    @property
    def module_installed(self) -> bool:
        return self.module_name in sys.modules

    @property
    def has_installed_version(self) -> bool:
        if not self.ext_dir.is_dir():
            return False
        return Path(self.ext_dir, "config.json").is_file()

    @property
    def installed_version(self) -> str:
        if self.installed_release:
            return self.installed_release.version
        return ""

    @property
    def requires_payment(self) -> bool:
        if not self.pay_to_enable:
            return False
        return self.pay_to_enable.required is True

    async def download_archive(self):
        logger.info(f"Downloading extension {self.name} ({self.installed_version}).")
        ext_zip_file = self.zip_path
        if ext_zip_file.is_file():
            os.remove(ext_zip_file)
        try:
            assert self.installed_release, "installed_release is none."

            self._restore_payment_info()

            await asyncio.to_thread(
                download_url, self.installed_release.archive_url, ext_zip_file
            )

            self._remember_payment_info()

        except Exception as exc:
            logger.warning(exc)
            raise AssertionError("Cannot fetch extension archive file") from exc

        archive_hash = file_hash(ext_zip_file)
        if self.installed_release.hash and self.installed_release.hash != archive_hash:
            # remove downloaded archive
            if ext_zip_file.is_file():
                os.remove(ext_zip_file)
            raise AssertionError("File hash missmatch. Will not install.")

    def extract_archive(self):
        logger.info(f"Extracting extension {self.name} ({self.installed_version}).")
        Path(settings.lnbits_extensions_path, "upgrades").mkdir(
            parents=True, exist_ok=True
        )

        tmp_dir = Path(settings.lnbits_data_folder, "unzip-temp", self.hash)
        shutil.rmtree(tmp_dir, True)

        with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
            zip_ref.extractall(tmp_dir)
        generated_dir_name = os.listdir(tmp_dir)[0]
        shutil.rmtree(self.ext_upgrade_dir, True)
        shutil.copytree(
            Path(tmp_dir, generated_dir_name),
            Path(self.ext_upgrade_dir),
        )
        shutil.rmtree(tmp_dir, True)

        # Pre-packed extensions can be upgraded
        # Mark the extension as installed so we know it is not the pre-packed version
        with open(Path(self.ext_upgrade_dir, "config.json"), "r+") as json_file:
            config_json = json.load(json_file)

            self.name = config_json.get("name")
            self.short_description = config_json.get("short_description")

            if (
                self.installed_release
                and self.installed_release.is_github_release
                and config_json.get("tile")
            ):
                self.icon = icon_to_github_url(
                    self.installed_release.source_repo, config_json.get("tile")
                )

        shutil.rmtree(self.ext_dir, True)
        shutil.copytree(Path(self.ext_upgrade_dir), Path(self.ext_dir))
        logger.success(f"Extension {self.name} ({self.installed_version}) installed.")

    def clean_extension_files(self):
        # remove downloaded archive
        if self.zip_path.is_file():
            os.remove(self.zip_path)

        # remove module from extensions
        shutil.rmtree(self.ext_dir, True)

        shutil.rmtree(self.ext_upgrade_dir, True)

    def check_latest_version(self, release: Optional[ExtensionRelease]):
        if not release:
            return
        if not self.latest_release:
            self.latest_release = release
            return
        if version_parse(self.latest_release.version) < version_parse(release.version):
            self.latest_release = release

    def find_existing_payment(
        self, pay_link: Optional[str]
    ) -> Optional[ReleasePaymentInfo]:
        if not pay_link:
            return None
        return next(
            (p for p in self.payments if p.pay_link == pay_link),
            None,
        )

    def _restore_payment_info(self):
        if not self.installed_release:
            return
        if not self.installed_release.pay_link:
            return
        if self.installed_release.payment_hash:
            return
        payment_info = self.find_existing_payment(self.installed_release.pay_link)
        if payment_info:
            self.installed_release.payment_hash = payment_info.payment_hash

    def _remember_payment_info(self):
        if not self.installed_release or not self.installed_release.pay_link:
            return
        payment_info = ReleasePaymentInfo(
            amount=self.installed_release.cost_sats,
            pay_link=self.installed_release.pay_link,
            payment_hash=self.installed_release.payment_hash,
        )
        self.payments = [
            p for p in self.payments if p.pay_link != payment_info.pay_link
        ]
        self.payments.append(payment_info)

    @classmethod
    def from_row(cls, data: dict) -> InstallableExtension:
        meta = json.loads(data["meta"])
        ext = InstallableExtension(**data)
        if "installed_release" in meta:
            ext.installed_release = ExtensionRelease(**meta["installed_release"])
        if meta.get("pay_to_enable"):
            ext.pay_to_enable = PayToEnableInfo(**meta["pay_to_enable"])
        if meta.get("payments"):
            ext.payments = [ReleasePaymentInfo(**p) for p in meta["payments"]]

        return ext

    @classmethod
    def from_rows(cls, rows: Optional[list[Any]] = None) -> list[InstallableExtension]:
        if rows is None:
            rows = []
        return [InstallableExtension.from_row(row) for row in rows]

    @classmethod
    async def from_github_release(
        cls, github_release: GitHubRelease
    ) -> Optional[InstallableExtension]:
        try:
            repo, latest_release, config = await cls.fetch_github_repo_info(
                github_release.organisation, github_release.repository
            )
            source_repo = f"{github_release.organisation}/{github_release.repository}"
            return InstallableExtension(
                id=github_release.id,
                name=config.name,
                short_description=config.short_description,
                stars=int(repo.stargazers_count),
                icon=icon_to_github_url(
                    source_repo,
                    config.tile,
                ),
                latest_release=ExtensionRelease.from_github_release(
                    source_repo, latest_release
                ),
            )
        except Exception as e:
            logger.warning(e)
        return None

    @classmethod
    def from_explicit_release(cls, e: ExplicitRelease) -> InstallableExtension:
        return InstallableExtension(
            id=e.id,
            name=e.name,
            archive=e.archive,
            short_description=e.short_description,
            icon=e.icon,
            dependencies=e.dependencies,
        )

    @classmethod
    async def get_installable_extensions(
        cls,
    ) -> list[InstallableExtension]:
        extension_list: list[InstallableExtension] = []
        extension_id_list: list[str] = []

        for url in settings.lnbits_extensions_manifests:
            try:
                manifest = await cls.fetch_manifest(url)

                for r in manifest.repos:
                    ext = await InstallableExtension.from_github_release(r)
                    if not ext:
                        continue
                    existing_ext = next(
                        (ee for ee in extension_list if ee.id == r.id), None
                    )
                    if existing_ext:
                        existing_ext.check_latest_version(ext.latest_release)
                        continue

                    ext.featured = ext.id in manifest.featured
                    extension_list += [ext]
                    extension_id_list += [ext.id]

                for e in manifest.extensions:
                    release = ExtensionRelease.from_explicit_release(url, e)
                    existing_ext = next(
                        (ee for ee in extension_list if ee.id == e.id), None
                    )
                    if existing_ext:
                        existing_ext.check_latest_version(release)
                        continue
                    ext = InstallableExtension.from_explicit_release(e)
                    ext.check_latest_version(release)
                    ext.featured = ext.id in manifest.featured
                    extension_list += [ext]
                    extension_id_list += [e.id]
            except Exception as e:
                logger.warning(f"Manifest {url} failed with '{e!s}'")

        return extension_list

    @classmethod
    async def get_extension_releases(cls, ext_id: str) -> list[ExtensionRelease]:
        extension_releases: list[ExtensionRelease] = []

        for url in settings.lnbits_extensions_manifests:
            try:
                manifest = await cls.fetch_manifest(url)
                for r in manifest.repos:
                    if r.id != ext_id:
                        continue
                    repo_releases = await ExtensionRelease.get_github_releases(
                        r.organisation, r.repository
                    )
                    extension_releases += repo_releases

                for e in manifest.extensions:
                    if e.id != ext_id:
                        continue
                    explicit_release = ExtensionRelease.from_explicit_release(url, e)
                    await explicit_release.check_payment_requirements()
                    extension_releases.append(explicit_release)

            except Exception as e:
                logger.warning(f"Manifest {url} failed with '{e!s}'")

        return extension_releases

    @classmethod
    async def get_extension_release(
        cls, ext_id: str, source_repo: str, archive: str, version: str
    ) -> Optional[ExtensionRelease]:
        all_releases: list[ExtensionRelease] = (
            await InstallableExtension.get_extension_releases(ext_id)
        )
        selected_release = [
            r
            for r in all_releases
            if r.archive == archive
            and r.source_repo == source_repo
            and r.version == version
        ]

        return selected_release[0] if len(selected_release) != 0 else None

    @classmethod
    async def fetch_github_repo_info(
        cls, org: str, repository: str
    ) -> tuple[GitHubRepo, GitHubRepoRelease, ExtensionConfig]:
        repo_url = f"https://api.github.com/repos/{org}/{repository}"
        error_msg = "Cannot fetch extension repo"
        repo = await github_api_get(repo_url, error_msg)
        github_repo = GitHubRepo.parse_obj(repo)

        lates_release_url = (
            f"https://api.github.com/repos/{org}/{repository}/releases/latest"
        )
        error_msg = "Cannot fetch extension releases"
        latest_release: Any = await github_api_get(lates_release_url, error_msg)

        config_url = f"https://raw.githubusercontent.com/{org}/{repository}/{github_repo.default_branch}/config.json"
        error_msg = "Cannot fetch config for extension"
        config = await github_api_get(config_url, error_msg)

        return (
            github_repo,
            GitHubRepoRelease.parse_obj(latest_release),
            ExtensionConfig.parse_obj(config),
        )

    @classmethod
    async def fetch_manifest(cls, url) -> Manifest:
        error_msg = "Cannot fetch extensions manifest"
        manifest = await github_api_get(url, error_msg)
        return Manifest.parse_obj(manifest)


class CreateExtension(BaseModel):
    ext_id: str
    archive: str
    source_repo: str
    version: str
    cost_sats: Optional[int] = 0
    payment_hash: Optional[str] = None


class ExtensionDetailsRequest(BaseModel):
    ext_id: str
    source_repo: str
    version: str
