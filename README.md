Requirements:
-------------
grako
svgwrite

TODO / Considerations:
---------------------
* Get rid of services and notes
* Change grammar to have a fixed set of primitives

* '.' would be a more obvious and conventional choice than '->' unless the names on the left of the '->' have a much weirder meaning than I think
* referring to '()' as "brackets" is slightly more confusing than calling them parentheses (as brackets can also be '[ ]')
* grammar seems to be casual about some things and strict about others---primitives are completely unrestricted, for example, but IP address literals
* it isn't immediately clear why particular names (such as those to the left of '->') are bound in particular places and have particular properties specified in particular places
