# PyGsiElev

This is a tiny Python package that can get the elevation of
specified coordinates, using the open DEM data distributed from GSI.

## Prepare data

- Download DEM data from [GSI's download service](https://fgd.gsi.go.jp/download/mapGis.php?tab=dem). The service is free of charge, but user registration is required.

- Place the downloaded files together in a directory of your choice.


## How to use

Import `pygsielev.ElevationExtractor` class and instanciate with `data_dir`.
Then, call `get_elevation()` of the object with longitude and latitude.

```
>>> from pygsielev import ElevationExtractor
>>> engine = ElevationExtractor(data_dir="data/")
>>> print(engine.get_elevation(lon=138.727299, lat=35.360785))
(3774.9, 'その他')
```

It returns a tuple contains (elevation, surface type).

Note: When the `data_dir` paramater is omitted, the environmental variable
`GSIELEV_DATADIR` will be used to get the data directory.

## Operating environment

This package works with Python 3.8 or later. It uses only the standard library.

## Contributing

Pull requests are welcome.

## Author

Takeshi Sagara <sagara@info-proto.com>

## License

This package can be used under the [MIT](https://choosealicense.com/licenses/mit/) License.
