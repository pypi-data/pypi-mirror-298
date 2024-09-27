from bs4 import (
    BeautifulSoup,
)
from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.location_read_closer import (
    LocationReadCloser,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.javascript.package import (
    package_url,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Package,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
import re

SCRIPT_DEP = re.compile(
    r"(?P<name>[^\s\/]*)(?P<separator>[-@\/])"
    r"(?P<version>(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*))"
)


def _get_location(location: Location, sourceline: int) -> Location:
    if location.coordinates:
        return location.model_copy(
            update={
                "coordinates": location.coordinates.model_copy(
                    update={"line": sourceline}
                )
            }
        )
    return location


def parse_html_scripts(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    try:
        html = BeautifulSoup(reader.read_closer, features="html.parser")
    except AssertionError:
        return [], []

    packages = [
        Package(
            name=matched.group("name"),
            version=matched.group("version"),
            licenses=[],
            locations=[_get_location(reader.location, script.sourceline)],
            language=Language.JAVASCRIPT,
            type=PackageType.NpmPkg,
            p_url=package_url(matched.group("name"), matched.group("version")),
        )
        for script in html("script")
        if (
            (src_attribute := script.attrs.get("src"))
            and src_attribute.endswith(".js")
            and (matched := SCRIPT_DEP.search(src_attribute))
        )
    ]
    return packages, []
