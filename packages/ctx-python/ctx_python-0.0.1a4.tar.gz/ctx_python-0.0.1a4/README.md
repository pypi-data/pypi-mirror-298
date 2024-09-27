# ctx-python

Python wrapper for U.S. EPA's Center for Computational Toxicology and Exposure (CTE) APIs.

## Installation
`ctx-python` is available to install via `pip`.

```
pip install ctx-python
```

## Initialization
**Before being able to access CCTE's API, a user must acquire an API key.** See [https://api-ccte.epa.gov/docs/](https://api-ccte.epa.gov/docs/) for more information.

Once an API key is obtained, `ctx-python` offers two options for passing the key for authentication:

1. Supply the key at the point of instantiatation for each domain. This will look something like:

```{python}
import ctxpy as ctx

chem = ctx.Chemical(x_api_key='648a3d70')
```

2. `ctx-python` comes with a command-line tool that will utilize the `.env` file that will store the key. If no key is supplied at instantiation, `ctx-python` will automatically attempt to load this file and use a key stored there.
```{bash}
[user@host~]$ ctx_init --x-api-key 648a3d70
```
This will result in the .env file having three new environment variables added to the file: `ctx_api_host`, `ctx_api_accept`, `ctx_x_api_key`.

```{python}
import ctxpy as ctx

chem = ctx.Chemical()
```

## Usage
The backbone of `ctx-python` is its base `Connection` class. This class takes the appropriate authentication key and other important information for GET and POST commands and stores them for each call to the API. There are 5 different domains that have a specific `Connection` sub-class:
- Chemical
- Exposure
- Hazard (comming soon)
- Bioactivity (comming soon)
- Ecotox (comming soon)

### Chemical
The `Chemical` class provides capabilities to:
- search for chemicals by their names, CAS-RNs, DTXSIDs, or other potential identifiers
- retrieve details about a chemical from a DTXSID (single chemical or batch search) or DTXCID (single chemical only)
- search for chemicals that match features common in Mass Spectrometry (i.e., a range of molecular mass, chemical formula, or by DTXCID)

```{python}
import ctx

# Start an instance of the Chemical class
chem = ctx.Chemical()

# Search for some data
chem.search(by='equals',word='toluene')
chem.search(by='starts-with',word='atra')
chem.search(by='contains',word='-00-')
chem.search(by='batch',word=['50-00-0','BPA'])


# Get some chemical details
chem.details(by='dtxsid', word='DTXSID7020182')
chem.details(by='dtxcid', word='DTXCID701805')
chem.details(by='batch', word=['DTXSID7020182','DTXSID3021805'])

# Search for some MS info
chem.msready(by='dtxcid',word='DTXCID30182')
chem.msready(by='formula', word='C17H19NO3')
chem.msready(by='mass', start=200.9, end=200.93)
```

### Exposure
The `Exposure` class provides capabilities to:
- search for a chemical's:
    - reported functional use information
    - predicted functional uses
    - presence in consumer/industrial formulations or articles
    - presence in annotated chemical list
- retrieve controlled vocabularies for:
    - Function Categories (FC)
    - Product Use Categories (PUC)
    - List Presence Keywords (LPKs)

```{python}
import ctx

# Start an instance of the Exposure class
expo = ctx.Exposure()

# Search for some data
expo.search(by="fc",word="DTXSID7020182")
expo.search(by='qsur',word='DTXSID7020182')
expo.search(by='puc',word='DTXSID7020182')
expo.search(by='lpk', word='DTXSID7020182')


# Get controlled vocabularies
expo.vocabulary(by='fc')
expo.vocabulary(by='puc')
expo.vocabulary(by='lpk')
```

## Disclaimer
This software/application was developed by the U.S. Environmental Protection Agency (USEPA). No warranty expressed or implied is made regarding the accuracy or utility of the system, nor shall the act of distribution constitute any such warranty. The USEPA has relinquished control of the information and no longer has responsibility to protect the integrity, confidentiality or availability of the information. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the USEPA. The USEPA seal and logo shall not be used in any manner to imply endorsement of any commercial product or activity by the USEPA or the United States Government.
