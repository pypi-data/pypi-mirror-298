# sopel-rainbow

A Sopel plugin to make things RAINBOW COLORED.

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-rainbow
```

## Configuring

The easiest way to configure `sopel-rainbow` is via Sopel's configuration
wizard—simply run `sopel-plugins configure rainbow` and enter the values for
which it prompts you.

### `order` setting

By default, `sopel-rainbow` outputs colors in the "standard" rainbow `order`,
ROYGBIV, subject to receiving clients' use of the customary meanings for IRC
color codes 0-15. If set explicitly in your Sopel config file, this default
value would look like:

```ini
[rainbow]
order =
    4
    7
    8
    3
    12
    2
    6
```

If you want to get creative (or cater to a community with shared color norms
that differ from the "de facto" values established by mIRC and friends)
override the `order` with your own list of _numeric_ codes:

```ini
[rainbow]
order = # Americans and French can fight over this one
    4
    0
    2
```

### `random_start` setting

Starting the rainbow at the beginning of the `order` every time is also
default behavior. If you want the rainbow to start at a random place every
time instead, set the Boolean option `random_start` to `yes` or `on`:

```ini
[rainbow]
random_start = on
```

## Dependencies

* Sopel version 7.1 or higher
* Python 3.8 or higher

Sopel 7.x should still run on Python 2.7 or older Python 3 releases, but it's
not maintained any more; and neither is this plugin tested on anything older.
