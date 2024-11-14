# TestMeli

You must run the program and then a swagger screen will open up where you will have two methods
a get method that will return this format
```
[
  {
    "count_human_dna": Number,
    "count_mutant_dna": Number,
    "ratio": Number
  }
]
```

Method post, we must pass through the body a list of characters that form strings of dna, they can only be valid characters,
such as A T C G, it will return 200 and a message saying that it is a mutant in case it is and in case it is a human it will return 401 and it will say that you are not authorized.
401 and say that you are not authorized, although the information will be saved anyway.

```
401 message: Is Human
or 
200 message: Is Mutant
```
