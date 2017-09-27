#!/bin/sh -e

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi

set -x

PYTHONPATH=. ${PREFIX}pytest ${@}
