#!/bin/zsh

source venv/bin/activate
# time
DATE=$(date +%Y_%m_%d_%H_%M_%S)
DPATH=Model/$DATE

if [ ! -x "$DPATH" ]; then
    mkdir $DPATH
fi
echo $DPATH

# generate dataset
python gen_data_train.py Model/$DATE/train.ffm Model/$DATE/valid.ffm
python gen_data_test.py Model/$DATE/test.ffm

# train & predict
./ffm-train -r 0.2 -p Model/$DATE/valid.ffm -s 8 --auto-stop Model/$DATE/train.ffm Model/$DATE/baseline.model
./ffm-predict Model/$DATE/test.ffm Model/$DATE/baseline.model Model/$DATE/output

# convert result
python convert2res.py Model/$DATE/output Model/$DATE/output.txt