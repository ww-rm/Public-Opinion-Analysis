CURPATH=$(cd "$(dirname "$0")"; pwd)
cd $CURPATH

if [! -d "env"]; then
    ENV_PY="env/bin/python3"
else
    ENV_PY="python3"
fi

$ENV_PY -m crawlers && \
$ENV_PY -m hotspot && \
$ENV_PY -m kgraph && \
$ENV_PY gendb.py