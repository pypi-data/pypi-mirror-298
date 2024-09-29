from pydantic import BaseModel
from typing import Optional, List, Tuple
from enum import IntEnum

class ProductGroupDescription(BaseModel):
    """
    Model representing a product group description.

    Attributes:
        productGroupName (str): The name of the product group.
        fadnProducts (List[Tuple[str, float]]): List of FADN codes included in the group and their representativeness.
        organic (int): Indicates if the product group is conventional (0), organic (1), or undetermined (2).
    """
    # Name of the product group in the population
    productGroupName: str
    # List of the fadn codes included in this group and their representativeness (0..100) over the total group
    fadnProducts: List[Tuple[str, float]]
    # 0 if the product group is conventional, 1 if it is organic, 2 if it is undetermined
    organic: int
    
class ProductionDataEntry(BaseModel):
    """
    Model representing a production data entry.

    Attributes:
        productGroupName (str): The name of the product group.
        nuts3 (str): The NUTS3 code for which this production data applies.
        production (float): The amount of produced units for this product.
    """
    # Name of the product group
    productGroupName: str
    # NUTS3 code for which this production data applies
    nuts3: str
    # Amount of produced units for this product
    production: float

class DataToPMM(BaseModel):
    """
    Model representing the data to be sent to PMM.

    Attributes:
        productList (List[ProductGroupDescription]): List of product group descriptions.
        yearNumber (int): The year for which the data is requested.
        simulationRequested (bool): Indicates if simulation data is requested.
        actualDataRequested (bool): Indicates if actual historical data is requested.
        nuts3List (List[str]): List of NUTS3 codes for which the data is requested.
        expectedProduction (List[ProductionDataEntry]): List of expected production for each product group/region.
    """
    productList: List[ProductGroupDescription]
    # Year for which the data is requested
    yearNumber: int
    # True if we desire to receive the estimation of this data only accounting with previous years data
    simulationRequested: bool
    # True if we desire to receive the actual historical value for this year, should it exists
    actualDataRequested: bool
    # List of the NUTS3 codes for which the data is requested
    nuts3List: List[str]
    # List of expected production for each product group / region, so the impact on the price can be calculated.
    expectedProduction: List[ProductionDataEntry]    

class IndividualPrice(BaseModel):
    """
    Model representing an individual price.

    Attributes:
        productGroupName (str): The name of the product group.
        nuts3 (str): The NUTS3 code for which this production data applies.
        simulatedPrice (float): The simulated price [€/unit] for this product.
        actualPrice (float): The actual price [€/unit] for this product in the historical data.
    """
    # Name of the product group
    productGroupName: str
    # NUTS3 code for which this production data applies
    nuts3: str
    # Price [€/unit] for this product
    simulatedPrice: float
    # Price [€/unit] for this product in the historical data. 0 if not available
    actualPrice: float
    
class DataFromPMM(BaseModel):
    """
    Model representing the data received from PMM.

    Attributes:
        prices (List[IndividualPrice]): List of individual prices.
        yearNumber (int): The year for which the data is related to.
    """
    prices: List[IndividualPrice]
    # Year for which the data is related to
    yearNumber: int