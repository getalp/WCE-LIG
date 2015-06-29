######################################################################
### Authors: Tien Ngoc Le & Tan Ngoc Le
### Homepage: tienhuong.weebly.com
### Email: letien.dhcn@gmail.com; letan.dhcn@gmail.com
### Created Date: 2014.05.12
### Updated Date: 2014.05.14
######################################################################

#!/usr/bin/perl -w

use strict;

open (FileRead, "$ARGV[3]");
open (FileWrite, ">$ARGV[4]");

#TienNLe disabled 2014.05.20
#print FileWrite "<$ARGV[0] setid=\"TienNLe_TanNLe\" srclang=\"$ARGV[1]\" trglang=\"$ARGV[2]\">\n";
#<?xml version="1.0" encoding="UTF-8"?>
print FileWrite "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
print FileWrite "<!DOCTYPE article PUBLIC \"-//OASIS//DTD DocBook XML V4.1.2//EN\" \"http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd\">\n";

print FileWrite "<article lang=\"\">\n";

my $lineNumber= 0;
while (<FileRead>)
{
	chomp;
	$lineNumber++;
	
	#TienNLe updated 2014.05.20
	#print FileWrite "<seg id=\"$lineNumber\"> $_ </seg>\n";
	print FileWrite "<para> $_ </para>\n";
}

print FileWrite "</article>\n";

#TienNLe disabled 2014.05.20
#print FileWrite "</$ARGV[0]>";

close (FileRead);
close (FileWrite);
