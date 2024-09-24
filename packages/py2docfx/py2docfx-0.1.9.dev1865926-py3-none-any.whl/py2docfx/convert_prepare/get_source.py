import os.path as path
import os
import subprocess
import sys
import time
import py2docfx.convert_prepare.git as git
import py2docfx.convert_prepare.pip_utils as pip_utils
import py2docfx.convert_prepare.pack as pack
from py2docfx.convert_prepare.package_info import PackageInfo
from py2docfx.convert_prepare.source import Source

YAML_OUTPUT_ROOT =  path.join("target_repo", "docs-ref-autogen")

def update_package_info(pkg: PackageInfo, source_folder: str):
    cur_path = os.getcwd()
    os.chdir(source_folder) # TODO: replace it

    all_files = os.listdir()
    files = [f for f in all_files if path.isfile(f)]

    # update package attributes
    attrs = ["name", "version", "author"]
    if "setup.py" in files:
        for attr in attrs:
            proc_ret = subprocess.run(
                ["python", "setup.py", "--quiet", "--dry-run", f"--{attr}"],
                capture_output=True,
                text=True,
                check=True
            )

            if isinstance(proc_ret.stdout, list):
                attr_val = (proc_ret.stdout[-1]).strip()
            elif '\n' in proc_ret.stdout:
                attr_val = proc_ret.stdout.strip().split('\n')[-1]
            else:
                attr_val = proc_ret.stdout.strip()

            setattr(pkg, attr, attr_val)
    else:
        folder = next(
            f for f in all_files if path.isdir(f) and f.endswith(".dist-info")
        )
        if folder:
            if path.exists(path.join(folder, "METADATA")):
                with open(
                    path.join(folder, "METADATA"), "r", encoding="utf-8"
                ) as file_handle:
                    metadata = file_handle.readlines()
                for meta_info in metadata:
                    meta_info_array = meta_info.split(":")
                    meta_field = meta_info_array[0].strip().lower()
                    if meta_field in attrs:
                        setattr(
                            pkg,
                            meta_field,
                            ":".join(meta_info_array[1:]).strip(),
                        )
            else:
                package_full_name = path.basename(folder)
                package_info = package_full_name.replace(
                    ".dist-info", "").split("-")
                pkg.name = "-".join(package_info[0:-1]).strip()
                pkg.version = package_info[-1].strip()

    # update package path
    os.chdir(cur_path) # TODO: replace it
    yaml_output_folder = path.join(YAML_OUTPUT_ROOT, pkg.name)
    pkg.path = Source(
        source_folder=source_folder, yaml_output_folder=yaml_output_folder, package_name=pkg.name
    )

def get_source(pkg: PackageInfo, cnt: int, vststoken=None, githubtoken=None):
    path_cnt = str(cnt)
    dist_dir = path.join("dist_temp", path_cnt)

    if pkg.install_type == PackageInfo.InstallType.SOURCE_CODE:
        start_time = time.time()
        if pkg.url:
            repo_folder = path.join("source_repo", path_cnt)
            token = githubtoken if "github.com" in pkg.url else vststoken
            source_folder = git.clone(
                repo_location=pkg.url,
                branch=pkg.branch,
                folder=repo_folder,
                extra_token=token,
            )
            if pkg.folder:
                source_folder = path.join(source_folder, pkg.folder)
        else:
            source_folder = pkg.folder
            sys.path.insert(0, source_folder)
        end_time = time.time()
        print(f"<download_source>{pkg.name},{end_time-start_time}<download_source/>")
    elif pkg.install_type == PackageInfo.InstallType.PYPI:
        full_name = pkg.get_combined_name_version()
        start_time = time.time()
        pip_utils.download(
            full_name,
            dist_dir,
            extra_index_url=pkg.extra_index_url,
            prefer_source_distribution=pkg.prefer_source_distribution,
        )
        end_time = time.time()
        print(f"<download_pypi>{pkg.name},{end_time-start_time}<download_pypi/>")
        start_time = time.time()
        # unpack the downloaded wheel file.
        downloaded_dist_file = path.join(dist_dir, os.listdir(dist_dir)[0])
        pack.unpack_dist(downloaded_dist_file)
        os.remove(downloaded_dist_file)
        source_folder = path.join(
            path.dirname(downloaded_dist_file),
            os.listdir(dist_dir)[0]
        )
        end_time = time.time()
        print(f"<unpack_pypi>{pkg.name},{end_time-start_time}<unpack_pypi/>")
    elif pkg.install_type == PackageInfo.InstallType.DIST_FILE:
        start_time = time.time()
        pip_utils.download(pkg.location, dist_dir, prefer_source_distribution=False)
        end_time = time.time()
        print(f"<download_dist>{pkg.name},{end_time-start_time}<download_dist/>")

        start_time = time.time()
        # unpack the downloaded dist file.
        downloaded_dist_file = path.join(dist_dir, os.listdir(dist_dir)[0])
        pack.unpack_dist(downloaded_dist_file)
        os.remove(downloaded_dist_file)
        if downloaded_dist_file.endswith(".tar.gz"):
            downloaded_dist_file = downloaded_dist_file.rsplit(".", maxsplit=1)[
                0]
        source_folder = path.join(
            path.dirname(downloaded_dist_file),
            os.listdir(dist_dir)[0]
        )
        end_time = time.time()
        print(f"<unpack_dist>{pkg.name},{end_time-start_time}<unpack_dist/>")
    else:
        raise ValueError(f"Unknown install type: {pkg.install_type}")

    start_time = time.time()
    update_package_info(pkg, source_folder)
    end_time = time.time()
    print(f"<update_package_info>{pkg.name},{end_time-start_time}<update_package_info/>")
