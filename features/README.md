# Texture Matching using Local Binary Patterns (LBP)
## Usage

__Perform training using__

```
python perform-training.py -t data/lbp/train/ -l data/lbp/class_train.txt

```

__Perform testing using__

```
python perform-testing.py -t data/lbp/test/ -l data/lbp/class_test.txt
```

__Perform SVM testing using__

```
python trainsvm.py -n data/lbp/<path to negative set>/ -p data/lbp/<path to positive set>/

python trainsvm.py -n data/Others/ -p data/StopSign/
```
