# SFISOP package


The purpose of this package is to contain all the needed models in one package.


# Installation

```bash
pip install sfisop
```
```bash
pip install --upgrade sfisop
```

```python
# Example of using one of the subpackages
from sfisop.datamodels.tsdatamodel.metadata import *
import sfisop.datamodels.tsdatamodel.tsdata_utils as tsdata_utils
from sfisop.datamodels.tsdatamodel.timeseriesdata import *

from sfisop.messaging_sdk.subscriber import SubscriberClient
from sfisop.messaging_sdk.publisher import PublisherClient

from sfisop.data_forwarder.forwarder.mongodb.mongodb_client import MongoDBClient
from sfisop.data_forwarder.forwarder.mongodb.mongodb_config import get_mongodb_forwarder_config
from sfisop.data_forwarder.forwarder.mongodb import mongodb_utils as utils

from sfisop.data_forwarder.forwarder.thingspeak.thingspeak_client import ThingsPeakClient
from sfisop.data_forwarder.forwarder.thingspeak.thingspeak_config import get_thingspeak_forwarder_config
import sfisop.data_forwarder.forwarder.thingspeak.thingspeak_utils as utils

# Your code here
```

## Contact

If you have any questions or need support, feel free to reach out:

- **Author**: Yosafe Fesaha Oqbamecail
- **Email**: [581515@stud.hvl.no](mailto:581515@stud.hvl.no)

We appreciate any feedback or contributions to make these packages even better!