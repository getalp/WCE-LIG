#!/bin/bash
cd /home/lent/Develops/DevTools/moses/bin/
/data1/home/lent/Develops/DevTools/moses/bin/extractor  --scconfig case:true  --scfile run2.scores.dat --ffile run2.features.dat -r /home/lent/Develops/Experiments/EMS_System_FR_EN/preprocessed/dev/dev.en -n run2.best100.out.gz
