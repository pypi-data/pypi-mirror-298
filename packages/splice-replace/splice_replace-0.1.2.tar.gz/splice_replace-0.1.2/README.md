# Splice Replace

`splice-replace` is a Python utility to extract, process, and replace text in a file by running an external script on the extracted text.

## Usage

```bash
./splice_replace.py <script_to_run> <file_path> <start_line> <start_col> <end_line> <end_col>
./splice_replace.py 'sed s/big/small/' myfile.txt 2 10 4 15
```

## Example

### Use sed on section of file:
```bash
echo "01 First Line" > myfile.txt
echo "02 Second Line" >> myfile.txt
echo "03 Third Line" >> myfile.txt
echo "04 Fourth Line" >> myfile.txt
echo "05 Fifth Line" >> myfile.txt

./splice_replace.py 'sed s/Second/2nd/' myfile.txt 2 1 2 17
```

Which results in the file:
```
01 First Line
02 2nd Line
03 Third Line
04 Fourth Line
05 Fifth Line
```

### Use sort on section of file:
```bash
echo "01 MUPPET CHARACTERS" > myfile.txt
echo "02 HERE IS A LIST OF MUPPET CHARACTERS ALPHABETICALLY" >> myfile.txt
echo "03" >> myfile.txt
echo "Kermit" >> myfile.txt
echo "Gonzo" >> myfile.txt
echo "Beaker" >> myfile.txt
echo "Animal" >> myfile.txt
echo "Fozzie Bear" >> myfile.txt
echo "09" >> myfile.txt
echo "10 THAT CONCLUDES THE LIST" >> myfile.txt

./splice_replace.py 'sort' myfile.txt 4 1 9 1
```

Which results in the file:
```
01 MUPPET CHARACTERS
02 HERE IS A LIST OF MUPPET CHARACTERS ALPHABETICALLY
03
Animal
Beaker
Fozzie Bear
Gonzo
Kermit
09
10 THAT CONCLUDES THE LIST
```

## Installation

### From source:
```bash
git clone
cd splice-replace
pip install -r requirements.txt
python setup.py install
```

### Using pip:
```bash
pip install splice-replace
```

## Motivation

Intellij IDEA has a feature called "External Tools" which allows you to run external scripts. You can pass the script
special variables like `$FilePath$`, `$SelectionStartLine$`, `$SelectionStartColumn$`, `$SelectionEndLine$`, and `$SelectionEndColumn$`.
I wanted to be able to configure the external tool to run a script on a selection of text in a file such that the script receives
that selection as stdin and gives the replacement as stdout. IntelliJ IDEA does not support this feature directly, so I wrote this utility.

For example if you wanted to run the `sort` command on a selection of text in a file, you could configure an external tool to run.
First, you would create the external tool in Settings -> Tools -> External Tools, then give it a name like "sort", set the program to
`/path/to/splice-replace` and the arguments to `"sort" $FilePath$ $SelectionStartLine$ $SelectionStartColumn$ $SelectionEndLine$ $SelectionEndColumn$`.

Then you could select a section of text in a file and run the external tool "sort" on that selection.

Of course, you can replace sort with your own utility or script.


