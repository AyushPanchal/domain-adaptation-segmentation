# Remote Training Notes

This project is designed so dataset preparation and result collection can happen
locally, while training can run on Kaggle or college GPU servers.

## Environment Variables

Training scripts should resolve paths from environment variables when present:

```bash
export DATA_ROOT=/path/to/data
export OUTPUT_ROOT=/path/to/runs
```

Kaggle example:

```bash
export DATA_ROOT=/kaggle/input/indraeye-mga
export OUTPUT_ROOT=/kaggle/working/runs
```

College GPU example:

```bash
export DATA_ROOT=/home/$USER/datasets/indraeye-mga
export OUTPUT_ROOT=/home/$USER/runs/domain-adaptation-segmentation
```

## Required Artifacts To Bring Back

For each experiment, copy back:

- `status.json`
- `timestamps.json`
- `command.txt`
- `stdout.log`
- `stderr.log`
- `results.csv`
- `metrics.json`
- `best.pt` or a note if weights are too large
- qualitative predictions, if generated

## Progress Visibility

Every training run should:

- stream output to terminal
- write output to `stdout.log` and `stderr.log`
- update `status.json`
- preserve partial logs on failure

