# Read in heudiconv docker image
FROM nipy/heudiconv


ENTRYPOINT ["/run.py"]
