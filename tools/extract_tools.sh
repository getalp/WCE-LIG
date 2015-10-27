#!/usr/bin/sh
# You need to install 7zip before
pushd terplus
7z e terp-pt.v1.tgz.7z.001
7z e terp.v1-2.tar.gz.7z.001
popd

pushd BabelSenseCount_v25
bzip2 -d BabelNet-API-2.5.tar.bz2
tar xvf BabelNet-API-2.5.tar
tar xvfz WordNet-3.0.tar.gz
7z e BabelNet-2.5.addons.tgz.7z.001
popd
