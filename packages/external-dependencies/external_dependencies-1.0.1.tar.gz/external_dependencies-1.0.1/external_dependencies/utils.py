




import os
import zipfile
from importlib.metadata import distributions

import boto3
from botocore import UNSIGNED
from botocore.config import Config

s3_resource = boto3.resource('s3', config=Config(signature_version=UNSIGNED))

def _list_external_dependencies() -> list:
    name_metadata_map = {
        dist.metadata['Name']: dist.metadata['Requires-External']
        for dist in distributions()
        if 'Requires-External' in dist.metadata
    }
    requires_external = []
    for name, requires in name_metadata_map.items():
        if type(requires) == str:
            requires_external.append(requires)
        elif type(requires) == list:
            requires_external.extend(requires)
    return list(set(requires_external))

def _filter_external_dependencies(deps: list[str], prefix: str) -> list:
    return [dep for dep in deps if dep.startswith(prefix)]

def _install_s3(dependencies: list[str], bucket_name: str, install_dir: str) -> None:
    if dependencies:
        print(f"Will install python 'Requires-External' for: {' '.join(dependencies)}")
        for dep in dependencies:
            print(f'Downloading {dep} from s3')
            bucket = s3_resource.Bucket(bucket_name)
            for obj in bucket.objects.filter(Prefix=f'{dep}/latest/'):
                if obj.key.endswith('/'):
                    continue  # Ignore directories
                filename = install_dir + obj.key.split('/')[-1]
                bucket.download_file(obj.key, filename)

                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    for file in zip_ref.filelist:
                        name = file.filename
                        if name.endswith('/'):
                            os.mkdir(os.path.join(install_dir, name))
                            os.chmod(os.path.join(install_dir, name), 0o755)
                        else:
                            outfile = os.path.join(install_dir, name)
                            with open(outfile, 'bw') as file_fs:
                                file_fs.write(zip_ref.read(name))
                            os.chmod(outfile, 0o755)
                os.remove(filename)

def _install_apt(dependencies: list[str]) -> None:
    if dependencies:
        print(f"Will install python 'Requires-External' for: {' '.join(dependencies)}")
        os.system(f'apt install {" ".join([dep for dep in dependencies])}')
    else:
        print('No external dependencies found')