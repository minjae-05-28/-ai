#!/bin/bash
cd /home/user/-ai
export PYTHONPATH=src
python3 scripts/run_forward_evolution.py --system extremophiles > results/forward_evolution/log_extremophiles.txt 2>&1
python3 scripts/run_forward_evolution.py --system parasites > results/forward_evolution/log_parasites.txt 2>&1
echo done > results/forward_evolution/ALL_DONE
