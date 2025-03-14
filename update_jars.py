from pathlib import Path

from cosmic_reach import versions as crversions


def main():
    versions = crversions.fetch()
    
    latest_client_version = max(filter(lambda v: v.client, versions.versions))
    latest_client_version.client.save(Path("client.jar"))
    
    latest_server_version = max(filter(lambda v: v.server, versions.versions))
    latest_server_version.server.save(Path("server.jar"))


if __name__ == "__main__":
    main()
