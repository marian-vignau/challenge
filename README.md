I started the proposed challenge and structured it as an utility script.

The provided format can be taken from another system or machine.

To run it, only use `python3 run.py employee_data.txt`. The script has builtin help showed using the --help option.

Testing it can be done using

`>>> python3 -m unittest.py` 

It was done using the standard library as asked, but it can be polished using a more modern alternative like pytest.

I decided to put the hour rates in a separated .ini file to allow easy changes, and even providing a new one in a new ini file for testing purpouses.

The code has this modules

- `run.py` as an entry point 
- `src.main` includes all the command line interface and input/output.
- `src.utils` has some functions used to compute times. This can be reused on multiple parts in a more complex system, and that was the reason to put them aside.
- `src.employee` include a dataclass used to store and format the output of Employee name and payments information.
- `src.rates` includes a class that parse, stores and apply hourly rates to data from employees. I used the standard ini format included in python's standard library because is clean, well known and has no overhead.
- `src.parse` includes parse_employee, takes one employee line and validates it. Every different malformation in the provided data was considered, and after raising an exception, the process can follow with the next employee.

I used the dataclass Employee to create a data structure to give the interfaces a well known format. This will be useful if this software is extended to include more functionality, like a new parser or importer from other sources.

The code is documented using comments, because this is readed inmediatly by other developers and can be used by tools like sphinx to generete documentation automatically.

