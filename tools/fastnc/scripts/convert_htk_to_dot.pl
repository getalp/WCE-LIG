#!/usr/bin/perl -w

use strict;
use warnings;

use Graph;
use Graph::Reader::HTK;
use Graph::Writer::Dot;

    
my $reader = Graph::Reader::HTK->new;
my $graph = $reader->read_graph($ARGV[0]);

my $writer = Graph::Writer::Dot->new();
$writer->write_graph($graph, "temp");

`dot -Tpng "temp" > "$ARGV[0]"."png"`
