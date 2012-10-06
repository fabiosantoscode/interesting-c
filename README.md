interesting-c
=============

A language based on C, compiling to C, and overcoming C's inherent stubbornness and error-prone syntax.

Why?
----

Because C is fast and it could also be easier to code! And because C macros are clunky and error-prone.

Purpose of interesting-c
------------------------

The purpose of the interesting-c language is to create a new language on top of C. This language will be able to use C's strengths together with modern languages' strengths, as well as surpass many of C's weaknesses. The syntax will be closely resemblant to C, but the language will attempt to discourage usage of odd C constructs as much as it can, avoiding programmer errors whenever possible.

One could mention the C++ language as a project already implementing the functionality expressed here in this document. However, C++ is far different from this. While C++ extends C and adds to it (every C++ program is a C program too), interesting-c is a juiced-up subset of C which compiles to pure C code. The interesting-c “compiler” is nothing more than a translator leveraging the standard C language to create fast programs which are easier to read and write than C or C++.

One of the main advantages of the language is the definition of a C interface. While it can create executables, it can also create shared libraries, automatically implementing a C interface.

Philosophy
----------

There are two core ideas behind interesting-c.

The first one, is to make a language derivative of C which is much easier to program in than the original C. By leveraging text processing and simple compile-time analysis of the code, we can do away with some complexity and error-proneness.

The second idea behind interesting-c is to ease metaprogramming. By introducing a pre-compilation step and giving access to pre-compile-time data to the runtime code, and allowing the programmer to intervene in this pre-compilation step, advanced reflection becomes available to extremely fast code.

For example, it is easier to expose a XML-RPC API if you have the access to all subclasses (or implementers), methods and their names, as well as argument names and types for every method. More can be done using this information, for instance, JSON serialization (any kind of serialization, for that matter), ORM systems, etc. 

Roadmap
-------

interesting-c is still a baby language. You're not yet capable of creating anything usable with it.

Since this is in an early stage, probably a lot of these are going to be dropped later or replaced with something better.

 * base language (basic C types (declared only on stack), arrays (mainly for strings), print statement, no functions, no pointers)
 * automatically wrap code to `int main` function, for short scripts.
 * inline functions, expanding as macros.
 * meta language (interesting-c meta templates) to replace macros.
 * `#define` and `#include` for co-op with C.
 * structs(objects)
 * a way to associate a header file to an interesting-c file. And throw a compiler error when you forget to define or declare something on either side.
 * print
 * interesting-c meta services (the `__meta__` object)
    * One is able to easily get a list of all the properties anything has, as well as get property values and types by name, etc.
 * modules, importing
 * "C mode", to switch to C.
 * "C mode" for the meta language.
 * Name mangling when variables are beyond the variable name truncation limit (31 characters), to avoid name collisions. In "C mode", name mangling is not possible and raises a compilation error.
 * resolve import dependencies to avoid double `#include` and wan users of redefinitions
 * multiline strings with ''' or """, or heredoc. 
 * Raw strings, to write regexes or windows paths.
 * properties, inspired in C# properties.
 * function decorators (`@decorator <whitespace and/or newline> function`) (create code before and after function call, replace function with decorator. see python decorators.)
 * tags (`#tagname`) for methods and attributes. Their only purpose is to help search methods in the `__meta__` object. For example, a xml or JSON serializer might look only for attributes with `#serializeme` set.
 * function guards `int func(int a>0){...} int func2(int a<=0){...}`
 * list and mapping syntatic sugar
 * `pointer to <type>` syntax
 * pointers. Abstract `->` into `.`.
 * smart pointers for any occasion. You should be able to use a lot of pointers without crying with fear. Try to do intelligence in the compile time related to the pointer type, and avoid any overhead related to garbage collection, refcounting, etc.
 * `pointer to {signature}` point to a struct each function declared in signature and the instance variable.
 * `point <pointer> to <pointer or heap resource>`. Re-points a pointer to something else. Forces this "something else" to be a heap resource if it is a stack resource (changes its declaration).
 * applying mappings and arrays as function arguments.
 * `polymorphic`
 * capsule definition `[abstract] capsule <capsule name><template declarations> (of pointer to private LinkedListNode<T>) [(when <interface which inherits the capsule>)]`
 * capsules
 * capsule|module standard methods (`__call__`, `__int__`, `__main__`, `__export__`)
 * abstract (inherit-only) capsules
 * capsule inheritance
 * Unicode strings.
 * No function replacement when function arguments are the ellipsis, and when the function gets called with said ellipsis.
 * wraps
 * signatures of objects (`{int get_id(), string get_name()}`) to specify a desired signature for an object. They are of the special type "signature" and may be used without name.
 * a `foreach` construct.
 * wrap guards `<wrap name> (for <signature>)`
 * call arguments by name, fill in defaults automatically.
 * capsule inheritance guards (implemented in compile-time)
 * templates (?)
 * Operator overloading
 * template choice `(constructor declaration) <template name> becomes [typeof]<argument name>` (?)
 * `(|loose|own|...) pointer to <type>`
 * different kinds of pointer behavior
 * read imported C code
 * closures
 * A standard event loop (as seen in ECMAscript). This is to avoid having the programmer create his own event loop system. It should also be possible to use third-party event loops.
 * signature bool arithmetic. Compute several signature tests into one `Hashable = {bytes hash} || {}` (only common interface will be available for use).
 * signature mergers (to compensate for signatures not having all required methods, signature mergers will compensate by implementing some functions using result from others.)
 * Standard interfaces using signature bool arithmetic and smart merges (E.G. Iterable, Hashable...).

