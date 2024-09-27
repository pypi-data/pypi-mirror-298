from contextlib import (
    suppress,
)
from fluid_sbom.pkg.cataloger.redhat.rpmdb import (
    berkeley,
    sqlite,
)
from fluid_sbom.pkg.cataloger.redhat.rpmdb.entry import (
    header_import,
)
from fluid_sbom.pkg.cataloger.redhat.rpmdb.errors import (
    InvalidDBFormat,
)
from fluid_sbom.pkg.cataloger.redhat.rpmdb.package import (
    get_nevra,
    PackageInfo,
)
from fluid_sbom.pkg.cataloger.redhat.rpmdb.rpmdb_interface import (
    RpmDBInterface,
)


class RpmDB:  # pylint:disable=too-few-public-methods
    def __init__(self, database: RpmDBInterface) -> None:
        self.database = database

    def list_packages(
        self,
    ) -> list[PackageInfo]:
        packages: list[PackageInfo] = []
        for entry in self.database.read():
            try:
                index_entries = header_import(entry)
            except ValueError as exc:
                raise ValueError("Failed to import header") from exc
            if index_entries:
                package = get_nevra(index_entries)
                packages.append(package)
        return packages


def open_db(file_path: str) -> RpmDB | None:
    with suppress(InvalidDBFormat):
        return RpmDB(sqlite.open_sqlite(file_path))
    with suppress(InvalidDBFormat):
        return RpmDB(berkeley.BerkeleyDB(file_path))
    return None
