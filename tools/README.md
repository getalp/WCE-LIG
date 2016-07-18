# New (V1.5)

BebelNet is not needed anymore, you can use <STRONG> DBnary </STRONG> to replace the data used by BabelNet. The scores obtained are the same and the process time is strongly shorter!
You still can you BebelNet if you wish to.


# Tools directory

List of files to decompress before (you need tar, gzip and bzip2 before):
+ ./BabelSenseCount_v25/BabelNet-API-2.5.tar.bz2
+ ./BabelSenseCount_v25/WordNet-3.0.tar.gz

List of files to decompress with 7zip (you need to install 7zip before):
+ ./terplus/terp.v1-2.tar.gz.7z.{001-014}
+ ./terplus/terp-pt.v1.tgz.7z.{001-002}
+ ./BabelSenseCount_v25/BabelNet-2.5.addons.tgz.7z.{001-019}

A script enable this extraction automatically (extract_tools.sh)


# BabelNet Configuration

After the decompression, please, put the correct paths to these files (full path is needed):
+tools/BabelSenseCount_v25/BabelNet-2.5/config/babelnet.var.properties:	the value "babelnet.dir"
+tools/BabelSenseCount_v25/BabelNet-2.5/config/jlt.var.properties:	the value "jlt.wordnetPrefix"

