
# -*- coding: utf-8 -*-
# Copyright (c) 2010--2012  Peter Dinges <pdinges@acm.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
Field related classes and functions (field as in rational, real, or
complex numbers).

@package   fields
@author    Peter Dinges <pdinges@acm.org>
"""

class Field:
    """
    A base class for field elements that provides default operator overloading.
    
    For example, subtraction is defined as addition of the additive inverse.
    Derived classes therefore only have to implement the following operations
    to support the complete operator set:
    - __bool__(): Zero testing (@c True if not zero)
    - __eq__(): Equality testing with the @c == operator (@c True if equal)
    - __add__(): Addition with the @c + operator; @c self is the left summand
    - __neg__(): Negation with the @c - unary minus operator (the additive inverse)
    - __mul__(): Multiplication with the @c * operator; @c self is the
      left factor
    - multiplicative_inverse(): Reciprocal (the multiplicative inverse)
    
    The following operations are implemented in terms of above operations using
    the field axioms:
    - __neq__(): Inequality testing with the @c != operator
    - __radd__(): Addition with the @c + operator; @c self is the right summand
    - __sub__(): Subtraction with the @c - operator; @c self is the minuend
      (left element)
    - __rsub__(): Subtraction with the @c - operator; @c self is the
      subtrahend (right element)
    - __rmul__(): Multiplication with the @c * operator; @c self is the
      right factor
    - __truediv__(): Division with the @c / operator; @c self is the
      dividend (left element)
    - __rtruediv__(): Division with the @c / operator; @c self is the
      divisor (right element) 
    - __pow__(): Exponentiation with integers
    """
    
    #- Template Operations ---------------------------------------------------- 
    
    def __neq__(self, other):
        """
        Test whether another element @p other is different from @p self; return
        @c True if that is the case.  The infix operator @c != calls this
        method; for example:
        @code
        if self != other:
            do_something()
        @endcode
        """
        return not self.__eq__( other )
    
    def __radd__(self, other):
        """
        Return the sum of @p self and @p other.  The infix operator @c + calls
        this method if @p self is the right summand and @p other.__add__()
        returns @c NotImplemented. For example:
        @code
        result = other + self
        @endcode
        """
        return self.__add__( other )
    
    def __sub__(self, other):
        """
        Return the difference of @p self and @p other.  The infix operator @c -
        calls this method if @p self is the minuend (left element); for example:
        @code
        result = self - other
        @endcode
        """
        return self.__add__( -other )
    
    def __rsub__(self, other):
        """
        Return the difference of @p other and @p self.  The infix operator @c -
        calls this method if @p self is the subtrahend (right element) and
        @c other.__sub__() returns @c NotImplemented.  For example:
        @code
        result = other - self
        @endcode
        """
        # other - self == -(self - other)
        return -self.__sub__( other )
    
    def __rmul__(self, other):
        """
        Return the product of @p self and @p other.  The infix operator @c *
        calls this method if @p self is the right factor and @c other.__mul__()
        returns @c NotImplemented.  For example:
        @code
        result = other * self
        @endcode 
        """
        return self.__mul__( other )
    
    def __truediv__(self, other):
        """
        Return the quotient of @p self and @p other.  The infix operator @c /
        calls this method if @p self is the dividend; for example:
        @code
        result = self / other
        @endcode
        
        @exception ZeroDivisionError   if @p other is zero.
        @exception TypeError           if @p other lacks the
                                       multiplicative_inverse() method and
                                       cannot be cast to @p self's class.
        """
        if not other:
            raise ZeroDivisionError
        
        try:
            other = self.__class__(other)
            return self.__mul__( other.multiplicative_inverse() )
        
        except TypeError:
            return NotImplemented

    def __rtruediv__(self, other):
        """
        Return the quotient of @p other and @p self.  The infix operator @c /
        calls this method if @p self is the divisor and @c other.__truediv__()
        returns @c NotImplemented.  For example
        @code
        result = other / self
        @endcode
        
        @exception ZeroDivisionError   if @p self is zero.
        """
        return self.multiplicative_inverse() * other

    def __pow__(self, n):
        """
        Return @p self taken to the @p n-th power.  The infix operator @c **
        calls this method; for example:
        @code
        result = self ** n
        @endcode
        
        @note  The implementation uses the most naive by-the-book method for
               exponentiation: the element is multiplied @p n-1 times with
               itself.  This is slow (and might skin your cat!).  However, the
               purpose of this code is to be easy to understand, not fast. 
        
        @param n   The exponent; it is expected to be a non-negative integer
                   type.  Negative integers and floats are unsupported.
        """
        # This only makes sense for integer arguments.
        result = self
        for i in range(1, int(n)):
            result = result * self
        
        return result


    #- Base Operations (Defined in Derived Classes) ---------------------------
    
    def __bool__(self):
        """
        Test whether the element is non-zero: return @c True if, and only if,
        it is non-zero. Otherwise return @c False.  Implicit conversions to
        boolean (truth) values use this method; for example when @c x is an
        element of a Field:
        @code
        if x:
            do_something()
        @endcode
        
        @exception NotImplementedError if this method is called; subclasses
                                       must implement this operation.
        """
        raise NotImplementedError
    
    def __eq__(self, other):
        """
        Test whether another element @p other is equal to @p self; return
        @c True if that is the case.  The infix operator @c == calls this
        method; for example:
        @code
        if self == other:
            do_something()
        @endcode
        
        @exception NotImplementedError if this method is called; subclasses
                                       must implement this operation.
        """
        raise NotImplementedError
    
    def __add__(self, other):
        """
        Return the sum of @p self and @p other.  The infix operator @c + calls
        this method if @p self is the left summand; for example:
        @code
        result = self + other
        @endcode
        
        @exception NotImplementedError if this method is called; subclasses
                                       must implement this operation.
        """
        raise NotImplementedError
    
    def __neg__(self):
        """
        Return the additive inverse of @p self.  The unary minus operator @c -x
        calls this method; for example:
        @code
        negated = -self
        @endcode

        @exception NotImplementedError if this method is called; subclasses
                                       must implement this operation.
        """
        raise NotImplementedError
    
    def __mul__(self, other):
        """
        Return the product of @p self and @p other.  The infix operator @c + calls
        this method if @p self is the left factor; for example:
        @code
        result = self * other
        @endcode
        
        @exception NotImplementedError if this method is called; subclasses
                                       must implement this operation.
        """
        raise NotImplementedError
    
    def multiplicative_inverse(self):
        """
        Return the multiplicative inverse of @p self.

        @exception NotImplementedError if this method is called; subclasses
                                       must implement this operation.
        """
        raise NotImplementedError
 

# -*- coding: utf-8 -*-
# Copyright (c) 2010--2012  Peter Dinges <pdinges@acm.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
A naive implementation of fraction fields (rational fields over an
integral domain).

@package   fields.fraction.naive
@author    Peter Dinges <pdinges@acm.org>
"""

from Types import template
from Operators import operand_casting

@operand_casting
class FractionField( Field, metaclass=template("_integral_domain") ):
    """
    A field of formal quotients (fractions)
    @f$ \frac{\mathrm{numerator}}{\mathrm{denominator}} @f$ over an integral
    domain; the field elements support infix notation for field operations,
    and mixed argument types.

    This is a template class that must be instantiated with the underlying
    integral domain. For example:
    @code
    # Instantiate the template; Q is a class (here: the rational numbers)
    Q = FractionField( rings.integers.naive.Integers )
    x = Q(1, 2)    # Create a field element: one over two
    y = Q(2)       # Another field element: two, which is two over one
    z = x*y        # z is two over two; no canceling takes place
    z == Q(4, 4)   # This true because 4*2 == 2*4
    type(z) is Q   # This is also true
    @endcode

    A formal quotient is an equivalence class of pairs (numerator, denominator)
    whose entries come from an integral domain (a commutative ring with
    identity and no zero divisors). Two pairs @f$ \frac{u}{v} @f$ and
    @f$ \frac{s}{t} @f$ are considered equivalent if, and only if, @f$ u\cdot t
    = s\cdot v @f$. Observe that this comparison uses multiplication only;
    since the elements come from a ring and might have no multiplicative
    inverses, division does not work.
    
    @note  A consequence of omitted canceling is that the elements might grow
           large.
    
    @note  The class uses the operand_casting() decorator: @c other operands in
           binary operations will first be treated as FractionField elements.
           If that fails, the operation will be repeated after @p other was fed
           to the constructor __init__().  If that fails, too, then the
           operation returns @c NotImplemented (so that @p other.__rop__()
           might be invoked).
    
    @see   For example, Robinson, Derek J. S.,
           "An Introduction to Abstract Algebra", p. 113.
    """    
    def __init__(self, numerator, denominator=None):
        """
        Construct a new formal quotient (@p numerator, @p denominator).
        
        If the @p numerator is an element of this FractionField class, then
        the new element is a copy of @p numerator; @p denominator is ignored.
        Otherwise, a @c None denominator (the default) is interpreted as the
        multiplicative neutral element (one) in the underlying integral domain.
        
        @exception     ZeroDivisonError    if the denominator is zero (and not
                                           @c None, see above).
        """
        if isinstance(numerator, self.__class__):
            # Copy an instance
            self.__numerator = numerator.__numerator
            self.__denominator = numerator.__denominator
        
        else:
            if denominator is None:
                denominator = self._integral_domain.one()
            if not denominator:
                raise ZeroDivisionError
            self.__numerator = self._integral_domain( numerator )
            self.__denominator = self._integral_domain( denominator )


    def __bool__(self):
        """
        Test whether the formal quotient is non-zero: return @c True if, and
        only if, the numerator is non-zero. Return @c False if the numerator
        is zero.
        
        Implicit conversions to boolean (truth) values use this method, for
        example when @c x is an element of a FractionField:
        @code
        if x:
            do_something()
        @endcode
        """
        return bool( self.__numerator )
    

    def __eq__(self, other):
        """
        Test whether another formal quotient @p other is equivalent to @p self;
        return @c True if that is the case.  The infix operator @c == calls
        this method.
        
        Two fractions @f$ \frac{u}{v} @f$ and @f$ \frac{s}{t} @f$ are equivalent
        if, and only if, @f$ u\cdot t = s\cdot v @f$. 
        
        @note  Comparison may be expensive: it requires two multiplications in
               the underlying integral domain.
        """
        # Use the basic definition of equivalence for comparison.
        return self.__numerator * other.__denominator \
                == other.__numerator * self.__denominator
    

    def __add__(self, other):
        """
        Return the sum of @p self and @p other. The infix operator @c + calls
        this method.
        
        As usual, the sum of two fractions @f$ \frac{u}{v} @f$ and
        @f$ \frac{s}{t} @f$ is @f$ \frac{ u\cdot t + s\cdot v }{ v\cdot t } @f$.
        
        @note  Canceling of common factors is impossible, for the underlying
               integral domain contains non-units. Therefore, repeated addition
               results in large elements.
        """
        numerator = self.__numerator * other.__denominator \
                    + self.__denominator * other.__numerator
        denominator = self.__denominator * other.__denominator
        return self.__class__( numerator, denominator )


    def __neg__(self):
        """
        Return the additive inverse of @p self, which is @f$ \frac{-u}{v} @f$
        for a fraction @f$ \frac{u}{v} @f$. The negation operator @c -x
        (unary minus) calls this method.
        """
        return self.__class__(
                    -self.__numerator,
                    self.__denominator
                )
    

    def __mul__(self, other):
        """
        Return the product of @p self and @p other. The @c * infix operator
        calls this method.
        
        As usual, the product of two fractions @f$ \frac{u}{v} @f$ and
        @f$ \frac{s}{t} @f$ is @f$ \frac{ u\cdot s }{ v\cdot t } @f$.
        
        @note  Canceling of common factors is impossible, for the underlying
               integral domain contains non-units. Therefore, repeated
               multiplication results in large elements.
        """
        numerator = self.__numerator * other.__numerator
        denominator = self.__denominator * other.__denominator
        return self.__class__( numerator, denominator )
    

    def multiplicative_inverse(self):
        """
        Return the multiplicative inverse of @p self, which is
        @f$ \frac{v}{u} @f$ for a fraction @f$ \frac{u}{v} @f$.
        
        @exception ZeroDivisionError   if @p self is zero (has a zero numerator)
        
        @see   __bool__()
        """
        if not self:
            raise ZeroDivisionError
        
        return self.__class__(
                    self.__denominator,
                    self.__numerator
                )
    

    @classmethod
    def zero(cls):
        """
        Return the field's neutral element of addition (zero).
        
        Zero in a FractionField is a fraction @f$ \frac{0}{1} @f$, where
        @f$ 0 @f$ and @f$ 1 @f$ denote the zero and one of the underlying
        integral domain.
        """
        return cls( cls._integral_domain.zero(), cls._integral_domain.one() )

    
    @classmethod
    def one(cls):
        """
        Return the field's neutral element of multiplication (one).
        
        One (or unity) in a FractionField is a fraction @f$ \frac{1}{1} @f$,
        where @f$ 1 @f$ denotes the one of the underlying integral domain.
        """
        return cls( cls._integral_domain.one(), cls._integral_domain.one() )

