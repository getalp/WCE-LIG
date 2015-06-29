######################################################################
### Authors: Tien Ngoc Le & Tan Ngoc Le
### Homepage: tienhuong.weebly.com
### Email: letien.dhcn@gmail.com; letan.dhcn@gmail.com
### Created Date: 2014.05.12
### Updated Date: 2015.01.07
######################################################################

#!/usr/bin/perl -w

use strict;

open (FileRead, "$ARGV[3]");
open (FileWrite, ">$ARGV[4]");

print FileWrite "<$ARGV[0] setid=\"TienLe_TanLe\" srclang=\"$ARGV[1]\" trglang=\"$ARGV[2]\">\n";
print FileWrite "<DOC sysid=\"Tien_Tan_system\" docid=\"TienNgocLe_TanNgocLe\">\n";

my $lineNumber= 0;
while (<FileRead>)
{
	chomp;
	$lineNumber++;
	print FileWrite "<seg id=\"$lineNumber\"> $_ </seg>\n";
}

print FileWrite "</DOC>\n";
print FileWrite "</$ARGV[0]>";

close (FileRead);
close (FileWrite);
