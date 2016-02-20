#! /bin/sh


export PYTHONPATH=$PYTHONPATH:../../:../:../default_experiments/
make html
make latexpdf
