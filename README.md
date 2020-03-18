# lotterycreator

Exercise project for python learning.


The lottery tool accepts data files with lottery participant list, and returns a list of winners.
File can contain only names or names with weights assigned (higher or lower chances of winning).

## Usage:
* participants input file is given as command line argument
* format is given with `--format` option
* template file can be specified with `--template` option
* `--output` option allows specifying JSON report output file
* program looks for input files inside `../data/` directory (at same level as lotterycreator project directory)
* template files are in `../data/lottery_templates` if no name is given the first alphabetical name is taken as default

### data directory location

By default the directory is expected at same level as project directory.
```
.
├── data
└── lotterycreator
```

But you can set an envrironment variable `LOTTERY_DATA` that will override this location.
Keep in mind, that empty `LOTTERY_DATA` means current directory, and you need to `unset` it to go back to default.
