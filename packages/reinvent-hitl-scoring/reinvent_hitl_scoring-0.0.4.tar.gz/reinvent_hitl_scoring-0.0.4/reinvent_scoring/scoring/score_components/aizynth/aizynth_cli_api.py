"""AiZynthFinder command-line API.

For AiZynthFinder documentation, see:
- https://github.com/MolecularAI/aizynthfinder
- https://confluence.astrazeneca.com/display/AIZ/User+guide (internal)

This module provides two implementations:
- One that uses AiZynthFinder built-in parallelization
- One that uses SLURM for parallelization

SLURM appears to be more robust.
"""

import gzip
import json
import os
import pathlib
import shlex
import subprocess
import tempfile
from datetime import timedelta
from typing import List, Dict


# Configuration file to use for running AiZynthFinder on SCP.
# Future versions might switch to externally-provided file.
config = """
finder:
  properties:
    iteration_limit: 100
    return_first: false
    time_limit: {time_limit_seconds}
filter:
  aizynthfinder.az.filter_strategies.DisappearanceFilter:
    magic:
  files:
    full_set: /projects/mai/aizynthfinder_models/keras_models/full_set_filter/keras_model.hdf5
policy:
  files:    
    standard:
      - /projects/mai/aizynthfinder_models/keras_models/reaction_connect_expansion/keras_model.hdf5
      - /projects/mai/aizynthfinder_models/metadata/reaction_connect/unique_templates.csv.gz
stock:
  files:
    ACD: /projects/mai/databases/aizynth_buyables/aizynth_stock_20221114_ACD.hdf5
    ERM: /projects/mai/databases/aizynth_buyables/aizynth_stock_20221114_ERM.hdf5
    ISAC: /projects/mai/databases/aizynth_buyables/aizynth_stock_20221114_ISAC.hdf5
    """


def run_aizynthfinder_preallocated(smiles: List[str], time_limit_seconds: int) -> Dict:
    """Run AiZynthFinder on preallocated computing resources.

     This implementation uses AiZynthFinder built-in parallelization.

    :param smiles: list of SMILES strings
    :return: JSON dict with AiZynthFinder output
    """
    tmpdir = tempfile.mkdtemp(prefix="reinvent-aizynthfinder-", dir=os.getcwd())

    infile = pathlib.Path(tmpdir) / "input.smi"
    outfile = pathlib.Path(tmpdir) / "output.json.gz"
    configfile = pathlib.Path(tmpdir) / "config.yml"

    with open(configfile, "wt") as f:
        f.write(config.format(time_limit_seconds=time_limit_seconds))

    with open(infile, "wt") as f:
        f.writelines(s + "\n" for s in smiles)

    nproc = len(os.sched_getaffinity(0))  # https://stackoverflow.com/a/55423170

    cmd = f"conda run --prefix /projects/mai/mai_environments/aizynth-env aizynthcli --smiles {infile} --config {configfile} --policy standard --output {outfile} --nproc {nproc} --filter full_set magic"
    subprocess.run(shlex.split(cmd), cwd=tmpdir)

    # https://stackoverflow.com/a/39451012
    with gzip.open(outfile, 'r') as fin:
        out = json.loads(fin.read().decode('utf-8'))

    # Here we can clean up temp dir. Keep it for now for debug purposes.

    return out


def run_aizynthfinder_array(smiles: List[str], time_limit_seconds: int) -> Dict:
    """Run AiZynthFinder on newly-allocated SLURM array job.

    :param smiles: list of SMILES strings
    :return: JSON dict with AiZynthFinder output
    """
    tmpdir = tempfile.mkdtemp(prefix="reinvent-aizynthfinder-", dir=os.getcwd())

    infile_prefix = pathlib.Path(tmpdir) / "input"
    outfile_prefix = pathlib.Path(tmpdir) / "output"
    configfile = pathlib.Path(tmpdir) / "config.yml"
    scriptfile = pathlib.Path(tmpdir) / "slurm-aizynth.sh"

    with open(configfile, "wt") as f:
        f.write(config.format(time_limit_seconds=time_limit_seconds))

    for i, smi in enumerate(smiles, start=1):
        with open(f"{infile_prefix}_{i}.smi", "wt") as infile:
            infile.write(smi + "\n")

    extra_warmup_time_seconds = 120
    slurm_time = timedelta(seconds=(time_limit_seconds + extra_warmup_time_seconds))

    script = f"""#!/bin/bash
#SBATCH --array=1-{len(smiles)}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16gb
#SBATCH --time={slurm_time}
 
conda run --prefix /projects/mai/mai_environments/aizynth-env aizynthcli --smiles {infile_prefix}_${{SLURM_ARRAY_TASK_ID}}.smi --config {configfile} --output {outfile_prefix}_${{SLURM_ARRAY_TASK_ID}}.json.gz --policy standard --filter full_set magic
"""

    with open(scriptfile, "wt") as f:
        f.write(script)

    subprocess.run(["sbatch", "--wait", scriptfile], cwd=tmpdir)

    # Concatenate "data" sections from all output files.
    data = []
    for i in range(1, 1 + len(smiles)):
        # https://stackoverflow.com/a/39451012
        with gzip.open(f"{outfile_prefix}_{i}.json.gz", 'r') as fin:
            out_i = json.loads(fin.read().decode('utf-8'))
            data.extend(out_i["data"])

    out = {"data": data}

    # Write concatenated file, for debug purposes.
    with gzip.open(f"{outfile_prefix}.json.gz", 'w') as fout:
        fout.write(json.dumps(out).encode('utf-8'))

    # Here we can clean up temp dir. Keep it for now for debug purposes.

    return out
