![Sirius C*](https://cdn2.arqadium.com/f/72e5552c26814ba08fbe3ebd407480cb/unknown.png)

# Sirius C* compiler

_Experimental C* compiler, a language proof-of-concept_

Copyright © 2020-2021 Alexander Nicholi. All rights reserved.  
Released under Artisan Software Licence.  
Full terms in COPYING file or online: <https://aquefir.co/asl>

> Software engineering over the last fifteen to twenty-five years has become
> stunted. Increasingly less attention is paid to quality-of-work, and
> incredible amounts of resources are being spent to solve second order
> problems. Executives and engineers alike shoulder the blame for this, and
> the result is simply a whole lot of bad code. Peter Welch has mused much
> about the deplorable state of code quality in his semi-hyperbolic rant
> titled Programming Sucks. Bad code in a vacuum wouldn’t be a problem if it
> didn’t make it nearly impossible to write good code in an economically
> cohesive fashion. All of the code we have works together. If some bad code
> is sitting down the hierarchy, it can mess things up, lowering the quality
> baseline of all code running on a person’s machine. Programs need Law &
> Order, and where they need it most is with systems. Enter the programming
> language C*.

—Alexander Nicholi,  
excerpted from
[Law & Order in Software Engineering with C*](https://nicholatian.com/lawandorder).

-----

## Overview

C* is a modified version of ANSI C that has been completely reoriented around
Data-Oriented Design, as described in the book of the same name by Richard
Fabian. It offers new features like register structs for creating primitives,
a bit-oriented memory model with more straightforward access semantics, and
most importantly a concept of “law and order” to help programs manage their
expectations about the input data they deal with. It makes it practical to
build complex yet well-behaved systems by adding new semantics at the API
level for communicating and enforcing constraints upon plain old data types.

## Addressing complexity in systems

Practicality of complexity before now has always been achieved through
genericism. C* rejects this prescription, and instead capitalises on the
explicit semantics of C. Genericism is anathema to systems programming,
because it inherently obfuscates a program as a means to compartmentalise
complexity. This does not address the complexity in a way that programmers can
positively appreciate, rather trying to “do away” with it and let them pretend
it is something abstract when it is not. The complexity itself is already more
than enough for a human brain to handle – this abstract metaprogramming is
surely a denial of the system in any real mind and makes for bad systems.

Instead, C* capitalises on C’s communicativity to make obvious and clear the
details of a system. It then provides a slew of new semantic mechanisms for
constraining valid state, and a specification oriented around bits alone
instead of abstract objects or bytes of any length.

The essay entitled “Law & Order in Software Engineering with C*” proselytises
for C* through one of its key features: law & order. This is the part of C*
that provides fully arbitrary mutability of state.

### Laws

C* provides this through a few new keywords and a key concept. First among
these is the `law` keyword, which defines and optionally names constraints to
be used on data types. This is semantically accomplished through a series of
boolean expressions, like so:

    /* anonymous law applied to type */
    law : s32
    {
        _ >= 0;
        _ < 1000;
    };

    /* named law */
    law leet
    {
        _ == 1337;
    };

    /* applying previously declared law */
    law leet : u16;

These laws are enforced upon the data types they apply to at compile time
through an exhaustive program analysis. The compiler works backwards to create
a control flow tree representing a “transient variable lifetime”, and
exhaustively validates the initialisation and modifications of that transient
variable against the laws enacted upon it. This is made practical by
formalising the boundaries of the compilation unit as a border between
“native” and “foreign” code, which in the essay is called the total system.
Data which is confined to this total system gains the performance benefit of
fully arbitrary validity checking at compile time.

### Marshalling

To deal with foreign code, C* provides a mechanism called marshalling. This is
a definition of marshalling expanded from its current meaning in computer
science as a synonym for serialisation, to also include the act of validating
data being serialised according to arbitrary schemas, or in the case of C*,
arbitrary laws. All subroutines that are callable from outside the total
system must provide marshalling blocks for validating their variables, like
so:

    typedef u8 mybyte;

    law : mybyte
    {
        _ < 255;
        _ != 0;
    };

    void foo( mybyte a, int c )
    {
        /* marshalling happens one parameter at a time */
        marshal a
        {
            if( a == 0 )
            {
                /* a MUST be set to a valid value through marshalling
                 * but, we can check around that, smartly */
                a = 1;
                break;
            }

            /* exit the function otherwise */
            return;
        }

        /* this is the minimum required
         * if any laws enacted upon s32, this will fail to compile */
        marshal c
        { }

        /* alternatively, this minimal marshalling will do law checks
         * and return upon any failures, since marshal blocks are only
         * entered when the runtime checks for the laws fail */
        marshal c
        {
            return;
        }
    }

`marshal` blocks can only reference the parameter they are marshalling. They
may declare and modify local variables with automatic storage duration, and
may only call pure functions with such parameters.

## Fundamental model of data

C* models state in terms of bits. This is reflected in the type system: C* has
only one fundamental primitive type, the `bit`. All other primitives are
modeled as “register structs” of bits coupled with various attributes that the
compiler understands the meaning of.

### Memory model

C* has a simpler and more natural memory model improved upon from the memory
model of C. There are three types of memory and two jurisdictions of memory in
the language.

#### Types of memory

**Private memory:**  
Same as in OpenCL parlance; in CUDA terms it may be called “registers” or
“local memory”; in general-purpose CPU terms it is thread-local storage.
Writable, and only accessible from a single execution context.

**Shared memory:**  
Same as in CUDA parlance; in OpenCL terms it is called “local memory”; in CPU
terms it is typical, often heap-allocated memory. Writable and accessible from
potentially multiple concurrent execution contexts; this is the only memory
category that demands manual synchronisation.

**Constant memory:**  
Shared memory that is read-only for all execution contexts. This memory can be
shared and used without need for synchronisation across multiple execution
contexts, but is only modified at the moment it was declared.

#### Jurisdictions of memory

**Native memory:**  
Memory for which its entire lifetime and all of its access is confined to the
total system. Laws can be enacted upon types of objects residing in native
memory. Variable declarations default to this jurisdiction.

**Foreign memory:**  
Memory that may be accessed, created and/or destroyed outside of the total
system. All laws enacted on a type of object in foreign memory do not apply;
instead, the user must apply pacts and marshalling code to validate such data.
Use of either the extern or volatile storage modifiers declares a variable as
residing in foreign memory.

### Register structs

C* provides a new kind of `struct` to more precisely declare the anatomy of a
data type. Whereas normal `struct`s are a mechanism for declaring new complex
data types brought over from C, `register struct`s are a mechanism for
declaring new primitive data types. This is how it is possible for C* to have
only one fundamental primitive built-in to the language (the `bit`): the other
primitives programmers are used to having are declared in header files through
`register struct`s.

`register struct`s are often comprised of statically-sized arrays of bits or
other types. For example, a u8 is defined like so:

    typedef register struct
    {
        bit _[8];
    }
    u8;

This also uses a feature of C* called inline structs, which allows users to
declare a struct type with a single member named `_`, and access its instances
directly by name without any dot notation, like a primitive. 

### Attributes

An implementation will have a known list of attributes that convey certain
information about a new primitive. These are construed through a braced list
of string literals at the end of the `typedef`’s body, before the name, like
so:

    typedef register struct
    {
        bit _[8] { "signed2" };
    }
    s8;

The attribute `signed2` conveys that the number is signed using two’s
complement. This means the most significant bit of the type will be treated as
a sign bit by the implementation using two’s complement.

Some attributes and their provisions include:

| Name          | Explanation                            |
|---------------|----------------------------------------|
| `signed1`     | Signed integers using one’s complement |
| `signed2`     | Signed integers using two’s complement |
| `ieee-bin16`  | IEEE 754 floating point binary16       |
| `ieee-bin32`  | IEEE 754 floating point binary32       |
| `ieee-bin64`  | IEEE 754 floating point binary64       |
| `ieee-bin128` | IEEE 754 floating point binary128      |
| `ieee-bin256` | IEEE 754 floating point binary256      |
| `bigint`      | Unlimited precision integer            |

### A comprehensive, fluid ABI

C* strives to provide the maximum possible power to exactly specify the
function of a system. If a programmer needs a certain number, they need only
to declare as much specificity as they need, and the implementation has the
responsibility of discerning the best way to map that specificity onto the
targeted machine. When writing C, general-purpose "catch-all" primitives like
int and long often prove to be brittle, as they are, in fact, boiled down into
concrete types with more specificity than the programmer may have wanted. C*
takes the spirit of these built-in C primitives, as in their original intended
meaning from their names, and formalises that fluidity so it can be properly
taken advantage of by the programmer. If a programmer only needs so many bits
of information, they can cap it. If they need truly unbounded numbers, they
can use an attribute to ask the implementation for a number that can be
extended as large as needed.

The implementation has the responsibility of applying these definitions to
data through hardware-provided mechanisms for the sake of performance.
However, it is prudent for the system engineer to know the provisions and
limits of the hardware they are targeting, as C* will transparently fall back
to software emulation of unavailable features, in much the same way GCC has
fallback implementations of IEEE 754 floating-point arithmetic. Ultimately,
system engineers must fine tune their code if they desire the maximum possible
performance on a given machine.

The benefit of doing this in C* is that they simply need to understand the
hardware their code runs on; they do not always need to fall back to inline
assembly, whether it is to work around ABI formalities, or to have their
algorithms take advantage of important instructions like SSE or NEON when a
compiler might not emit them. Since the C* compiler models the program–machine
relationship so much better, it can be much more certain when things like
these are appropriate.
