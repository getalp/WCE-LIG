# Tools directory

List of files to decompress with 7zip (you need to install 7zip before):
+ ./terplus/terp.v1-2.tar.gz.7z.{001-014}
+ ./terplus/terp-pt.v1.tgz.7z.{001-002}
+ ./BabelSenseCount_v25/BabelNet-2.5.addons.tgz.7z.{001-019}

A script enable this extraction automatically (extract_tools.sh)

# BabelNet Configuration

After the decompression, please, put the correct paths to these files (full path is needed):
+tools/BabelSenseCount_v25/BabelNet-2.5/config/babelnet.var.properties:	the value "babelnet.dir"
+tools/BabelSenseCount_v25/BabelNet-2.5/config/jlt.var.properties:	the value "jlt.wordnetPrefix"

