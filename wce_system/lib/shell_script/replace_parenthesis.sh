#!/bin/bash
#
#######################################################################
#### Author: Tien Ngoc Le
#### Homepage: tienhuong.weebly.com
#### Email: letien.dhcn@gmail.com; letan.dhcn@gmail.com
#### Created Date: 2014.05.12
#### Updated Date: 2014.Dec.07
#######################################################################
#
#sed 's:(:[:g' < $1 > temp
#sed 's:):]:g' < temp > $2
#
#rm -rf temp
#
sed 's:(:[:g' < $1 | sed 's:):]:g' > $2
