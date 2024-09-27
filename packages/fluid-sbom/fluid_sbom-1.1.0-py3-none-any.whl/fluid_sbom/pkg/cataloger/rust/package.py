from fluid_sbom.internal.package_information.rust import (
    CRATES_ENDPOINT,
    get_cargo_package,
    Version,
)
from fluid_sbom.pkg.package import (
    Artifact,
    HealthMetadata,
    Package,
)
from fluid_sbom.utils.file import (
    Digest,
)
from packageurl import (
    PackageURL,
)


def _set_health_metadata_artifact(
    package: Package,
    current_package: Version | None,
) -> Package:
    if current_package and package.health_metadata:
        digest_value = current_package.get("checksum")
        package.health_metadata.artifact = Artifact(
            url=f"{CRATES_ENDPOINT}{current_package['dl_path']}",
            integrity=Digest(
                algorithm="sha256" if digest_value else None,
                value=digest_value,
            ),
        )
    return package


def complete_package(package: Package) -> Package:
    cargo_package = get_cargo_package(package.name)
    if not cargo_package:
        return package
    current_package = next(
        (
            version
            for version in cargo_package["versions"]
            if version["num"] == package.version
        ),
        None,
    )
    try:
        package.health_metadata = HealthMetadata(
            latest_version=cargo_package["crate"]["max_stable_version"],
            latest_version_created_at=(cargo_package["crate"]["updated_at"]),
        )
    except IndexError:
        return package
    package = _set_health_metadata_artifact(package, current_package)
    if (
        package.health_metadata
        and cargo_package["versions"][0]["published_by"]
    ):
        package.health_metadata.authors = cargo_package["versions"][0][
            "published_by"
        ]["name"]
    if (
        not package.licenses
        and (licenses := cargo_package["versions"][0].get("license"))
        and isinstance(licenses, str)
    ):
        package.licenses = [cargo_package["versions"][0]["license"]]

    return package


def package_url(name: str, version: str) -> str:
    return PackageURL(  # type: ignore
        type="cargo",
        namespace="",
        name=name,
        version=version,
        qualifiers=None,
        subpath="",
    ).to_string()
