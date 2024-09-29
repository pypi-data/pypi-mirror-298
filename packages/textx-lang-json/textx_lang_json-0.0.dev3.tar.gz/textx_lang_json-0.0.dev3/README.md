# textx-lang-json

![logos](https://github.com/Jean-Francois-Baget/textx-lang-json/blob/main/img/logos.jpg?raw=true)


**textx-lang-json** is a python implementation of the JSON (JavaScript Object Notation) data interchange format [RFC8259](https://www.rfc-editor.org/rfc/rfc8259) using the [textX](https://textx.github.io/textX/) meta-language. Though it is not intended to replace the standard python JSON encoder and decoder [Lib/json](https://docs.python.org/3/library/json.html), which is much faster, it is a good alternative when you want to mix some JSON in your own textX grammar, or a good starting point should you want to develop your own JSON-like grammar.

The `textxjson` package provides a parser (basically a *textX* *metamodel*), able to build a *textx* *model* from a JSON file or string. This model can be visualized, for educational purpose, but more importantly can be *decoded* to obtain the usual (as done by [Lib/json](https://docs.python.org/3/library/json.html)) python representation of the JSON document.

**textx-lang-json** has been created by Jean-François Baget at the [Boreal](https://team.inria.fr/boreal/) team ([Inria](https://www.inria.fr/fr) and [LIRMM](https://www.lirmm.fr/)). It is part of the [textx-lang-dlgpe]() project.

### Walkthrough

The following code demonstrates, in python, how to build a `parser`, generate a `model` from a python string respecting the JSON standard, and `decode` the model to obtain the usual python representation of the python string (in that case a dictionary). It also shows that `parser.model_from_str(data).decode()` returns the same python object as the standard `json.loads(data)`.

```python
from textx import metamodel_for_language

parser = metamodel_for_language('textxjson') # building the parser

data = '{"Hello": "World"}' # data is a python string respecting the JSON format
model = parser.model_from_str(data) # model is a JsonText object
textxresult = model.decode() # textxresult is a python dictionary

test1 = textxresult == {'Hello' : 'World'} # test1 is True

import json

jsonresult = json.loads(data) # using the standard python function to decode data

test2 = textxresult == jsonresult # test2 is True
```

Note that a parser can also read a JSON file:

```python
model = parser.model_from_file("./path/to/data.json")

```

## Installation

```
pip install textx-lang-json
```

### Testing

You can test that everything behaves correctly (but first you have to clone the whole repository).

```
git clone https://github.com/Jean-Francois-Baget/textx-lang-json.git
cd textx-lang-json
python -m unittest
```
```
..............
----------------------------------------------------------------------
Ran 14 tests in 11.538s

OK
```

Thanks to [ArenaNet](https://www.arena.net/) whose [GW2 API](https://wiki.guildwars2.com/wiki/API:Main) provided some data used in our testbed.

## Usage

### Building the parser

The first thing to do is to build the Json parser. This can be done with the following code.

```python
from textx import metamodel_for_language

parser = metamodel_for_language('textxjson')
```

#### Visualizing the grammar

This parser can be used to obtain a graphical representation of the grammar [json.tx](./src/textxjson/grammar/json.tx). For more details on textx visualization, see https://textx.github.io/textX/visualization.html.

```python
from textx.export import metamodel_export

metamodel_export(parser, 'json.dot')
```
This codes generates a file `json.dot` that can be visualized with [Graphviz](https://graphviz.org/), as shown below.

![parser](https://github.com/Jean-Francois-Baget/textx-lang-json/blob/main/img/json.png?raw=true)

### Parsing JSON

Most importantly, the parser can be used to generate a *model* from a python string encoding some JSON data, or directly from a JSON file.

#### Parsing a python string

The parsing below is demonstrated using a python string.

```python
some_json = r'''
{
    "name" : "textx-lang-json",
    "authors" : [
        "Jean-François Baget"
    ],
    "year" : 2024,
    "tested" : true
}
'''

model = parser.model_from_str(some_json)
```

#### Parsing a JSON file

If we have the following JSON file **data.json**...

```json
{
    "name" : "textx-lang-json",
    "authors" : [
        "Jean-François Baget"
    ],
    "year" : 2024,
    "tested" : true
}
```
... the parser can build the model directly from the file:

```python
model = parser.model_from_file("data.json")
```

#### Visualizing the model

As for the parser, the model can be visualized.

```python
from textx.export import model_export

model_export(model, 'model.dot')
```
This file `model.dot` can also be visualized with [Graphviz](https://graphviz.org/).


![model](https://github.com/Jean-Francois-Baget/textx-lang-json/blob/main/img/model.png?raw=true)

### Decoding the model

The method `decode()` is called on a *model* to obtain the usual python representation of JSON strings. The test shows the interest of this representation.

```python
result = model.decode()

test = result['authors'][0] == 'Jean-François Baget' # test is True
```





