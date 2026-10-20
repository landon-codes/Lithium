# Lithium
## By [landon-codes](https://github.com/landon-codes)
Lithium is an extremely minimal, and simple build system for C and C++.
It's sole purpose is to make the developer's life easier.

### What is it?
Lithium is a build system made for C and C++. It is designed to support all common complilers including:
1. clang (and clang++)
2. gcc (and g++)
3. mscv (cl)
4. tcc (limited support due to environment features)

The problem with many build systems is that they are compilated and difficult to start using.
Litium's goal is to lower the barrier to entry as low as it can go.

Lithium's three current commands are:
1. build (builds the project)
2. run (builds and runs the project)
3. getargs (gets the arguments that Lithium is using to compile)

Unlike other compilers, which used complicated configuration files, Lithium uses the simle .ini format for its configuration.

### Compiling
Lithium is written with Python. There are many ways to set up the project to make it easier to use.
The simplest way would be to just set up a script on your path that runs the python interperator to call this project.
You could also use a Python packager like Pyinstaller to package the application, them move it to somewhere on your path.
It is also possible to transcompile Python to C, which then allows you compile the project into native machine code.

### Running the App
The method you use may vary depending on which of the above methods you chose to package Lithium,
but overall running Lithium would look something like this:
```
application-name <arguments>
```

Lithium only has the three aforementioned commands, which are self explanitory:
1. `lithium build`
2. `lithium run`
3. `lithium getargs`

None of these commands take any arguments. All the information they need can either be inferred
or is contained in the configuration file that will be described below.

### Configuration
Lithium uses the .ini file format for configurations. It is simple to read, write, and parse.
Here is an example `lithium.ini` file:
```ini
[compilation]
compiler = clang++
standard = c++23

[build type]
type = standard
files = "main.cpp, a.cpp, b.cpp"
warning_error = true
output_name = bin/lithium
```

#### compiler
`compiler`, under the `[compilation]` section, is the name of the compiler that you will use for you project.
Lithium *does* specify between compiler variants (whether you are using C or C++).
If you are building a C++ project but you tell Lithium to use the "gcc" compiler, it will fail.
Make sure you give Lithium the correct compiler, whatever is input in the configuration file will
be the command that the application runs to compile the project.

If no compiler is given, Lithium will try to infer the compiler being used by
running their respective commands and seeing whether they fail or not.
If possible, always specify the compiler being used by the project, as the algorithm used
for inferring the compiler may fail.

#### standard
`standard`, under the `[compilation]` section is the standard that the project is using.
Just like `compiler`, this is a literal value and it will be passed to the compiler.
If an incorrect value is used for the standard the compiler will throw an error.

The standard can be ommited if it is not important. The compiler will instead use its default value.

#### extra_warnings
`extra_warnings`, under the `[compilation]` section enables extra warnings if set to `true`.
Ommiting this configuration default to false (or the default or your choice compiler).

#### warning_error
`warning_error`, under the `[compilation]` section compiles any warnings as errors when set to `true`.
Ommiting this configuration defaults to false.

#### enable_extensions
`enable_extensions`, under the `[compilation]` section disables compiler specific extensions
when set to `false`.
Ommiting this configuration defaults to true.

#### build_type
`type` under the `[build type]` section specifies the type of build that you are compiling.
The valid arguments are:
1. `standard` (the default)
2. `full build`
3. `unity`

`standard` compiles all new files used in the project into objects then links them as an executable.
This saves time in compiliing for large projects, as only files that have changed are recompiled. 
The `files` configuration can be set to tell the compiler what files are in your project.
The value of `files` is a comma seperated list of files wrapped in quotes. *You can see the example at the beginning of this section.*
If `files` is not provided, Lithium will try to auto detect the files in the project.
Regardless, it is reccomended to specify the files, as auto detection can fail.

`full build` takes every file and builds it the same as `standard`, but does not save or generate
object files. It creates a clean build every single time. It can take the files argument just the same as `standard` can.

`unity` takes one main file, which pulls in all the child files. Unity builds don't need header files since
their structure naturally handles collisions. However, an in depth explanation of unity builds
is out of the scope of this documentation.
`unity` also requires that `entry_point` is defined in you configuration. Under the same section,
`entry_point` is the main file that the compiler will need to compile in order to compile the project.
Unity builds only build one file, so `files` is not valid in combonation with `unity`; it will be ignored.

#### output_name
`output_name`, under the `[build type]` section specified the path of the final executable (and object files if generated).
Note that `output_name` does not take an extension. In an attempt to keep the application
cross platform, the Lithium automatically detects the correct
extension (or lack of so) for your project. You can also use this to specify the output
directory for your final executable. *The example above covers what was discussed here.*

If no configuration is set, the output defaults to `bin/main` (relative to the lithium.ini file). 

### Contributions
Contributions are welcome. Please submit an issue or pull request at the [GitHub repository](https://github.com/landon-codes/Lithium)
for any suggestions.

A discussions page should also be available on the GitHub repository.

### License
This project is under the terms of the Apache License 2.0.
See [LICENSE](LICENSE) for further details.
