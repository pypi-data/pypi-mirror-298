#!/usr/bin/env python3

""" Copyright 2024 Russell Fordyce

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
import textwrap
import time
import warnings

import numba
import sympy
from sympy.utilities.lambdify import MODULES as lambdify_modules

import numpy

__version__ = "1.3.0"  # lazy, see [ISSUE 32]

DTYPES_SUPPORTED = {
    # numpy.dtype("bool"):     1,
    numpy.dtype("uint8"):    8,
    numpy.dtype("uint16"):  16,
    numpy.dtype("uint32"):  32,
    numpy.dtype("uint64"):  64,
    numpy.dtype("int8"):     8,
    numpy.dtype("int16"):   16,
    numpy.dtype("int32"):   32,
    numpy.dtype("int64"):   64,
    numpy.dtype("float32"): 32,
    numpy.dtype("float64"): 64,
    # numpy.dtype("complex64"): 64,  # [ISSUE 36]
    # numpy.dtype("complex128"): 128,
}


def data_cleanup(data):
    """ verify the incoming data can be used

        currently this expects a dict of numpy arrays

        FUTURE optional other numpy-backed arrays support (ie. Pandas, Polars, etc.)
          for now, users can use the relevant .to_numpy() methods
          also consider .to_records()
    """
    if not data:
        raise ValueError("no data provided")
    if not isinstance(data, dict):
        raise TypeError(f"data must be a dict of NumPy arrays, but got {type(data)}")

    result = {}
    vector_length = {}
    for name, ref in data.items():
        # coerce single python values to 0-dim numpy values
        # FIXME makes even small values too wide (int64,float64)
        # FIXME may not handle very large or very small values
        if isinstance(ref, (int, float)):
            ref = numpy.array(ref)
        if not isinstance(ref, numpy.ndarray):
            raise TypeError(f"data must be a dict of NumPy arrays, but has member ({name}:{type(ref)})")
        if ref.dtype not in DTYPES_SUPPORTED:
            raise TypeError(f"unsupported dtype ({name}:{ref.dtype})")
        # NOTE single (ndim==0) values have shape==() and `len(array)` raises `TypeError: len() of unsized object`
        if ref.ndim == 0:
            vector_length[name] = 0
        elif ref.ndim == 1:
            vector_length[name] = len(ref)
        else:
            raise ValueError(f"only single values or 1-dimensional arrays are allowed, but got {name}:{ref.ndim}")
        vector_length[name] = 0 if ref.ndim == 0 else len(ref)
        result[name] = ref  # pack reference into collection

    # FUTURE support uneven input arrays when indexed [ISSUE 10]
    set_vector_lengths = set(vector_length.values())
    if len(set_vector_lengths - {0}) != 1:
        raise ValueError(f"uneven data lengths (must be all equal or 0 (non-vector)): {set_vector_lengths}")

    return result


def string_expr_cleanup(expr_string):
    """ a few rounds of basic cleanup to ease usage
        equality is transformed to Eq() form
            `LHS = RHS` -> `LHS==RHS` -> `Eq(LHS,RHS)`
    """
    # FUTURE reconsider if these can use the transformation subsystem
    if not isinstance(expr_string, str):
        raise ValueError("expr must be a string")

    if "<" in expr_string or ">" in expr_string:
        raise ValueError("inequality is not supported")

    # discard all whitespace to ease string processing
    expr_string = re.sub(r"\s+", r"", expr_string)  # expr_string.replace(" ", "")

    # coerce runs of "=" into exactly "=="
    # FIXME ideally only (0,1,2) exist, but let users be really excited ==== for now
    expr_string = re.sub(r"=+", "==", expr_string)
    count_equalities = expr_string.count("=") // 2
    if count_equalities > 1:  # not exactly 0 or 1 (==)
        raise SyntaxError(f"only 1 equivalence (==) can be provided, but parsed {count_equalities}: {expr_string}")
    elif count_equalities == 1:
        left, right = expr_string.split("==")
        # recurse for each half, then rejoin 'em
        left  = string_expr_cleanup(left)
        right = string_expr_cleanup(right)
        return f"Eq({left}, {right})"

    # user probably meant Pow() not bitwise XOR
    # FIXME add to warning subsystem `if "^" in expr_string:` and allow configuring
    expr_string = expr_string.replace("^", "**")

    # SymPy expects symbols to be separated from Numbers for multiplication
    #   ie. "5x+7" -> "5*x+7"
    # however, care needs to be taken to avoid splitting symbols and functions
    # which contain a number, like `t3`, `log2()`, etc.
    # currently considers only matches where a number appears directly after
    #   start of string | basic operators +-*/ | open parenthesis
    # and then a string starts (symbol)
    # likely this could be better tokenized by Python AST or SymPy itself
    expr_string = re.sub(r"(^|[\+\-\*\/]|\()(\d+)(\w)", r"\1\2*\3", expr_string)

    # make sure there's something left
    if not expr_string:
        raise ValueError("no content after cleanup")

    return expr_string


def string_expr_to_sympy(expr_string, name_result=None):
    """ parse string to a SymPy expression
        this is largely support logic to help sympy.parse_expr()
         - support for indexing Symbols via IndexBase[Idx]
         - helps make symbol reference collections consistent before and after parsing
           ie. `reference in e.atoms(IndexedBase)` or `foo is atom` are True

        note that  `parse_expr()` creates new symbols for any un-named values

        collections of Symbols are returned as dicts mapping {name:Symbol},
        even if there is only a single Symbol
        while any indexer (Idx) is returned as a mapping of
          {Idx:[low index,high index]}
        so the templated loop won't over or under-run its array indices
    """

    # collection of {name:Symbol} mappings for `sympy.parse_expr()`
    local_dict = {}

    # detect and manage relative offsets
    # FUTURE handle advanced relative indexing logic [ISSUE 11]
    offset_values = {}
    offset_range = [0, 0]  # spread amongst offsets as [min,max]
    for chunk in re.findall(r"(\w+)\[(.+?)\]", expr_string):
        base, indexing_block = chunk
        indexer = str(sympy.parse_expr(indexing_block).free_symbols.pop())
        try:  # extract the offset amount ie. x[i-1] is -1
            offset = sympy.parse_expr(indexing_block).atoms(sympy.Number).pop()
        except KeyError:
            offset = 0  # no offset like x[i]
        offset_range[0] = min(offset_range[0], offset)
        offset_range[1] = max(offset_range[1], offset)
        offset_values[base] = sympy.IndexedBase(base)
        offset_values[indexer] = sympy.Idx(indexer)
    local_dict.update(offset_values)

    # convert forms like `expr_rhs` into `Eq(result_lhs, expr_rhs)`
    verify_literal_result_symbol = False  # avoid NameError in later check
    if not expr_string.startswith("Eq("):
        if "=" in expr_string:
            raise RuntimeError(f"BUG: failed to handle equality during cleanup: {expr_string}")
        if name_result is None:
            verify_literal_result_symbol = True  # enable later warning path checks
            name_result = "result"
        # rewrite `expr_string` to `Eq()` form
        if offset_values:
            syms_result = sympy.IndexedBase(name_result)
            # FIXME indexer smuggled from above loop scope
            expr_string = f"Eq({syms_result}[{indexer}], {expr_string})"
        else:
            syms_result = sympy.Symbol(name_result)
            expr_string = f"Eq({syms_result}, {expr_string})"
        # pack result into locals before parse
        local_dict.update({name_result: syms_result})

    # FUTURE consider transformation system instead of direct regex hackery
    expr_sympy = sympy.parse_expr(expr_string, local_dict=local_dict)

    # assert there is only a single Idx
    # FUTURE multiple Idx can generate deeper loops
    indexers = expr_sympy.atoms(sympy.Idx)  # set of Symbols
    if len(indexers) > 1:
        raise ValueError(f"only a single Idx is supported, but got: {indexers}")

    if not expr_sympy.atoms(sympy.Eq):  # ensures (lhs,rhs) properties, alt: hasattr
        raise RuntimeError(f"BUG: didn't coerce into Eq(LHS, RHS) form: {expr_sympy}")

    # now (re-)extract the result Symbol from LHS
    # NOTE IndexedBase coerced to Symbol [ISSUE 9]
    atoms_lhs = expr_sympy.lhs.atoms(sympy.Symbol)
    # FUTURE opportunity to extract Number from LHS to fail or divide out
    if len(atoms_lhs) == 1:
        pass  # pop later, set of exactly 1 Symbol
    elif len(atoms_lhs) == 2:
        atoms_lhs = expr_sympy.lhs.atoms(sympy.IndexedBase)
        if len(atoms_lhs) != 1:
            raise ValueError(f"multiple possible result values: {atoms_lhs}")
    else:
        raise ValueError(f"multiple or no possible result values from LHS atoms:{atoms_lhs}")
    symbol_result = atoms_lhs.pop()  # now dissolve set: {x} -> x

    if name_result is not None and name_result != symbol_result.name:
        raise ValueError(f"mismatch between name_result ({name_result}) and parsed symbol name ({symbol_result.name})")

    # make dicts of {name: symbol} for caller
    # NOTE `symbol_result` must be last to simplify dropping via slicing in later logic
    symbols = {s.name: s for s in expr_sympy.atoms(sympy.Symbol) if s.name != symbol_result.name}
    symbols = {n: symbols[n] for n in sorted(symbols)}  # force lexical symbol ordering for consistency

    # make a dict (len==1) of the result symbol
    syms_result = {symbol_result.name: symbol_result}
    # now append it to the symbols dict so it can be an argument
    symbols.update(syms_result)  # always the last symbol

    # hint that user may be misusing "result" name in their RHS
    if verify_literal_result_symbol and (
        name_result in {a.name for a in expr_sympy.rhs.atoms(sympy.Symbol)}) and (
        name_result not in offset_values.keys()
    ):
        warnings.warn(
            "symbol 'result' in RHS refers to result array, but not indexed or passed as name_result",
            RuntimeWarning)

    # extract Idx value (exactly 0 or 1 value)
    syms_idx = {s.name: offset_range for s in indexers}
    if len(syms_idx) > 1:
        raise RuntimeError(f"BUG: too may Idx values: {syms_idx}")

    # FIXME atoms(Symbol) demotes IndexBase and Idx to Symbol in result [ISSUE 9]
    for name_idx in syms_idx.keys():  # expressly remove Idx names
        del symbols[name_idx]
    return expr_sympy, symbols, syms_idx, syms_result


def dtype_result_guess(expr, data):
    """ attempt to automatically determine the resulting dtype given an expr and data

        this is a backup where the user has not provided a result dtype
        possibly it could support warning for likely wrong dtype

        this is not expected to be a general solution as the problem is open-ended
        and likely depends on the real data

        WARNING this logic assumes the highest bit-width is 64
          larger widths will require rewriting some logic!
          intermediately a user should specify the type, assuming
          a (future) numba really has support for it
    """
    # set of dtypes from given data
    dtypes_expr = {c.dtype for c in data.values()}  # set of NumPy types

    # throw out some obviously bad cases
    if not dtypes_expr:
        raise ValueError("no data provided")
    dtypes_unsupported = dtypes_expr - set(DTYPES_SUPPORTED.keys())
    if dtypes_unsupported:
        raise TypeError(f"unsupported dtypes: {dtypes_unsupported}")

    if numpy.dtype("float64") in dtypes_expr:
        return numpy.dtype("float64")
    # promote 32-bit float to 64-bit when greater types are present
    max_bitwidth = max(DTYPES_SUPPORTED[dt] for dt in dtypes_expr)
    if numpy.dtype("float32") in dtypes_expr:
        if max_bitwidth > 32:
            return numpy.dtype("float64")
        return numpy.dtype("float32")

    # detect structures that make the result logically floating-point
    # TODO perhaps these should be part of a structured attempt to constrain inputs
    #   in addition to being available for guessing resulting type,
    #   even if the constraints are (initially) warns, not hard errors
    # see https://docs.sympy.org/latest/modules/functions/elementary.html
    if (
        expr.atoms(
            # straightforward floats
            sympy.Float,
            # trancendental constants
            sympy.pi,
            sympy.E,
            # FUTURE general scipy.constants support
            # common floating-point functions
            sympy.log,
            sympy.exp,
            # sympy.sqrt,  # NOTE simplifies to Pow(..., Rational(1,2))
            # sympy.cbrt,  #   can be found with expr.match(cbrt(Wild('a')))
            # trig functions
            sympy.sin, sympy.asin, sympy.sinh, sympy.asinh,
            sympy.cos, sympy.acos, sympy.cosh, sympy.acosh,
            sympy.tan, sympy.atan, sympy.tanh, sympy.atanh,
            sympy.cot, sympy.acot, sympy.coth, sympy.acoth,
            sympy.sec, sympy.asec, sympy.sech, sympy.asech,
            sympy.csc, sympy.acsc, sympy.csch, sympy.acsch,
            sympy.sinc,
            sympy.atan2,
            # LambertW?  # TODO is complex support actually extra work?
        ) or (
            # discover simple division
            # direct Integers are Rational, but fractional atoms are not Integer
            # additionally, simple divisions will simplify to Integer
            #   >>> parse_expr("4").atoms(Rational), parse_expr("4").atoms(Integer)
            #   ({4}, {4})
            #   >>> parse_expr("4/2").atoms(Rational), parse_expr("4/2").atoms(Integer)
            #   ({2}, {2})
            #   >>> e = "4/2*x + 1/3*y"
            #   >>> parse_expr(e).atoms(Rational) - parse_expr(e).atoms(Integer)
            #   {1/3}
            expr.atoms(sympy.Rational) - expr.atoms(sympy.Integer)
        ) or (
            # detect N/x constructs
            #   >>> srepr(parse_expr("2/x"))
            #   "Mul(Integer(2), Pow(Symbol('x'), Integer(-1)))"
            expr.match(sympy.Pow(sympy.Wild("", properties=[lambda a: a.is_Symbol or a.is_Function]), sympy.Integer(-1)))
        )
    ):
        if max_bitwidth <= 16:  # TODO is this a good assumption?
            return numpy.dtype("float32")
        return numpy.dtype("float64")

    # now pick the largest useful int
    # NOTE constant coefficients should all be Integer (Rational) if reached here

    w_signed   = 0  # NOTE Falsey
    w_unsigned = 0
    for dtype in dtypes_expr:
        if numpy.issubdtype(dtype, numpy.signedinteger):
            w_signed = max(w_signed, DTYPES_SUPPORTED[dtype])
        elif numpy.issubdtype(dtype, numpy.unsignedinteger):
            w_unsigned = max(w_unsigned, DTYPES_SUPPORTED[dtype])
        else:
            raise TypeError(f"BUG: failed to determine if {dtype} is a signed or unsigned int (is it a float?)")
    if w_signed and w_unsigned:
        raise TypeError("won't guess dtype for mixed int and uint, must be provided")
    if w_signed and not w_unsigned:
        return numpy.dtype("int64") if w_signed > 32 else numpy.dtype("int32")  # FUTURE >=
    if not w_signed and w_unsigned:
        return numpy.dtype("uint64") if w_unsigned > 32 else numpy.dtype("uint32")  # FUTURE >=

    raise TypeError(f"BUG: couldn't determine a good dtype for {dtypes_expr}")


def get_result_dtype(expr_sympy, results, data, dtype_result=None):
    """ ensure the result datatype matches what's given if any
        use a reasonable guess when not provided explicitly or via result data array
    """
    if results:
        name_result = next(iter(results.keys()))  # NOTE dict of 1 value
        try:
            dtype_data_result = data[name_result].dtype
        except KeyError:  # name not in in data (not passed: create array later)
            dtype_data_result = None
        else:  # data array contains result for dtype, if expressly provided too, ensure they match
            if dtype_result is None:
                dtype_result = dtype_data_result
            else:
                if dtype_data_result != dtype_result:
                    raise ValueError(f"passed mismatched result array ({dtype_data_result}) and result dtype ({dtype_result})")

    # if dtype_result is still None, guess or raise
    if dtype_result is None:
        dtype_result = dtype_result_guess(expr_sympy, data)

    if dtype_result not in DTYPES_SUPPORTED:
        raise RuntimeError(f"BUG: dtype_result ({dtype_result}) not in DTYPES_SUPPORTED")

    # definitely a supported NumPy type now
    return dtype_result


def signature_generate(symbols, results, data, dtype_result):
    """ generate a signature like
          `Array(int64, 1d, C)(Array(int64, 1d, C))`
        note that Arrays can be named and they begin with the name "array", which
          `repr()` -> `array(int64, 1d, C)`

        refer to Numba types docs and Numba Array(Buffer) classes for more details
          https://numba.readthedocs.io/en/stable/reference/types.html
    """
    # FUTURE support for names (mabye an upstream change to numba)
    #   likely further C-stlye like `void(int32 a[], int64 b)`
    # without names, the dtypes are positional, so ordering must be maintained
    # within logic that could reorder the arguments after fixing the signature!
    # however, when the user calls the Expressive instance,
    # data is passed as kwargs `fn(**data)` to the inner function
    mapper = []

    if len(results) != 1:
        raise RuntimeError("BUG: results symbols should have exactly 1 member: {results}")
    name_result   = next(iter(results.keys()))  # NOTE dict of len==1 if given
    result_passed = bool(name_result in data)  # directly check membership

    names_symbols = list(symbols.keys())
    if not result_passed:
        names_symbols.pop()  # drop the result name (guaranteed to be last symbol in dict)
    for name in names_symbols:  # use symbol ordering, not data ordering
        ref = data[name]
        # make a field like `array(int64, 1d, C)`
        dims   = ref.ndim
        layout = "C"  # FUTURE allow other layouts and use array method [ISSUE 35]
        dtype  = getattr(numba.types, str(ref.dtype))  # FIXME brittle, can `numba.typeof()` be used?
        field  = numba.types.Array(dtype, dims, layout)
        mapper.append(field)

    # TODO warn or raise if not all data names used (+config) [ISSUE 43]
    #   len() is sufficient (KeyError earlier if fewer, but may wrap that too)

    # now build complete signature for Numba to compile
    # FUTURE consider support for additional dimensions in result
    dtype = getattr(numba.types, str(dtype_result))
    return numba.types.Array(dtype, 1, "C")(*mapper), result_passed


def loop_function_template_builder(expr, symbols, indexers, results, result_passed, dtype_result):
    """ template workflow for indexed values
    """
    # build namespace with everything needed to support the new callable
    # simplified version of sympy.utilities.lambdify._import
    _, _, translations, import_cmds = lambdify_modules["numpy"]
    expr_namespace = {"I": 1j}  # alt `copy.deepcopy(lambdify_modules["numpy"][1])`
    for import_line in import_cmds:
        exec(import_line, expr_namespace)
    for sympyname, translation in translations.items():
        expr_namespace[sympyname] = expr_namespace[translation]

    # get ready to build the template
    name_result = next(iter(results.keys()))

    # construct further template components
    names_symbols = list(symbols.keys())
    if not result_passed:
        # drop the result from arguments
        names_symbols.pop()

    argsblock = ", ".join(names_symbols)

    # construct result block if needed
    # TODO simplify this logic
    if indexers:
        if result_passed:  # if the result array is passed in, just fill it by-index
            block_result = ""
        else:  # create an array to fill by-index
            block_result = f"{name_result} = numpy.full(length, numpy.nan, dtype={dtype_result})"
    else:  # not indexed
        if result_passed:
            # block_result = "f{name_result}"
            block_result = "[:]"  # broadcast to result array
        else:  # if result array is not passed, let LHS be created dynamically
            block_result = ""

    # FUTURE: need to manage this with [ISSUE 10] uneven arrays
    if result_passed:  # go ahead and use the passed array if possible
        sizer_name = name_result
    elif indexers:  # non-empty collection
        for symbol in expr.rhs.atoms(sympy.IndexedBase):
            sizer_name = symbol
            break
        else:
            raise RuntimeError("BUG: using template path without IndexedBase symbol")
    else:
        for symbol in expr.rhs.atoms(sympy.Symbol):
            if symbol.name == name_result:
                continue  # pragma nocover FIXME ordering depends on hash seeding PYTHONHASHSEED
            sizer_name = symbol
            break
        else:
            raise RuntimeError("BUG: couldn't determine size of result array")  # FIXME be clearer about why this happened

    # construct template
    if not indexers:
        T = """
        def expressive_wrapper({argsblock}):
            {lhs}{block_result} = {rhs}
            return {name_result}
        """.format(
            argsblock=argsblock,
            block_result=block_result,
            lhs=expr.lhs,
            rhs=expr.rhs,
            name_result=name_result,
        )
    elif len(indexers) == 1:
        indexer, (start, end) = next(iter(indexers.items()))
        # FIXME numpy.nan filler may not always be appropriate
        T = """
        def expressive_wrapper({argsblock}):
            length = len({sizer_name})
            {block_result}
            for {indexer} in range({start}, length - {end} + 1):
                {lhs} = {rhs}
            return {name_result}
        """.format(
            argsblock=argsblock,
            sizer_name=sizer_name,
            block_result=block_result,
            lhs=expr.lhs,
            rhs=expr.rhs,
            indexer=indexer,
            start=start,
            end=end,
            name_result=name_result,
        )
    else:
        raise RuntimeError(f"BUG: indexers must be len 1 when provided (see string_expr_to_sympy): {indexers}")

    # tidy up template
    T = textwrap.dedent(T)

    # build and extract
    exec(T, expr_namespace)
    fn = expr_namespace["expressive_wrapper"]

    return fn


class Expressive:

    def __init__(self, expr, name_result=None, *, config=None, allow_autobuild=False):
        # FUTURE make cleanup optional (arg or config)
        # FUTURE support passing SymPy expr [ISSUE 42]
        self._expr_source_string = string_expr_cleanup(expr)
        self._expr_sympy, self._symbols, self._indexers, self._results = string_expr_to_sympy(self._expr_source_string, name_result)

        # TODO config subsystem [ISSUE 29]
        "config hoopla"
        self.allow_autobuild = allow_autobuild

        self.signatures_mapper = {}

    def __str__(self):
        # NOTE unstable result for now
        return f"{type(self).__name__}({self._expr_sympy})"

    def __repr__(self):
        # NOTE unstable result for now
        # FUTURE display some major config settings (but most in a dedicated output)
        # FUTURE consider how to support or use `sympy.srepr()`
        # FUTURE consider mathjax, LaTeX, etc. display [ISSUE 17]
        content = [
            f"build_signatures={len(self.signatures_mapper)}",
            f"allow_autobuild={self.allow_autobuild}",
        ]
        return f"{str(self)} <{','.join(content)}>"

    def _prepare(self, data, dtype_result):
        """ prepare before build or __call__ """
        data = data_cleanup(data)
        dtype_result = get_result_dtype(self._expr_sympy, self._results, data, dtype_result)
        signature, result_passed = signature_generate(self._symbols, self._results, data, dtype_result)
        return data, dtype_result, signature, result_passed

    def build(self, data, *, dtype_result=None):  # arch target?
        """ compile function and collect it in signatures_mapper """
        data, dtype_result, signature, result_passed = self._prepare(data, dtype_result)

        expr_fn = loop_function_template_builder(
            self._expr_sympy,
            self._symbols,
            self._indexers,
            self._results,
            result_passed,
            dtype_result
        )

        built_function = numba.jit(
            signature,
            nopython=True,  # now the default
            # fastmath=True,  # FUTURE config setting [ISSUE 29]
            parallel=True,  # FUTURE config setting [ISSUE 29]
        )(expr_fn)

        self.signatures_mapper[signature] = built_function

        return self  # enable dot chaining

    def __call__(self, data, dtype_result=None):
        """ call the relevant compiled function for a particular data collection on it
            if signatures_mapper doesn't have the signature, allow_autobuild can be used
            to create it dynamically, though this loses a lot of the runtime execution speed
            benefits available to users who are able to pre-build for all the data
            signatures they have
        """
        data, dtype_result, signature, result_passed = self._prepare(data, dtype_result)

        try:
            fn = self.signatures_mapper[signature]
        except KeyError:
            if not self.allow_autobuild:
                raise KeyError("no matching signature for data: use .build() with representative sample data (or set allow_autobuild=True)")
            # FUTURE improve warning subsystem (never, once, each, some callback, etc.)
            #   further opportunity for dedicated config features
            # really it's important to alert users to a potential error, but not nanny 'em
            time_start = time.time()
            self.build(data, dtype_result=dtype_result)
            warnings.warn(f"autobuild took {time.time() - time_start:.2f}s (prefer .build(sample_data) in advance if possible)", RuntimeWarning)
            try:
                fn = self.signatures_mapper[signature]
            except KeyError:  # pragma nocover - bug path
                raise RuntimeError("BUG: failed to match signature after autobuild")

        return fn(**data)
