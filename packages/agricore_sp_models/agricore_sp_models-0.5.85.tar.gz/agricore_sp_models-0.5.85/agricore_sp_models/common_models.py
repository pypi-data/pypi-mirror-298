from re import S
from pydantic import BaseModel
from typing import Optional, List
from enum import IntEnum

class OrganicProductionType(IntEnum):
    """
    Enum representing the type of organic production.

    Attributes:
        Conventional (int): Conventional production.
        Organic (int): Organic production.
        Undetermined (int): Undetermined production type.
    """
    Conventional = 0
    Organic = 1
    Undetermined = 2
    
class FADNProductJsonDTO(BaseModel):
    """
    DTO representing a FADN product.

    Attributes:
        fadnIdentifier (str): The FADN identifier.
        description (str): Description of the product.
        productType (str): Type of the product.
        arable (bool): Indicates if the product is arable.
        representativenessOcurrence (Optional[float]): Representativeness occurrence of the product in the group.
        representativenessArea (Optional[float]): Representativeness area in hectares.
        representativenessValue (Optional[float]): Representativeness value in euros.
    """
    fadnIdentifier: str
    description: str
    productType: str
    arable: bool
    # The representativeness of the FADN product in the product group. Item representativeness should be calculated
    # as the representativeness of the FADN product divided by the sum of the representativeness of all FADN products in the product group.
    # For its calculation, remember than whe obtaining data from the sample, the weight of such farm in the population should be taken into account
    representativenessOcurrence: Optional[float] = None
    # In hectars
    representativenessArea: Optional[float] = None
    # In €
    representativenessValue: Optional[float] = None
    
class PolicyJsonDTO(BaseModel):
    """
    DTO representing a policy.

    Attributes:
        populationId (int): The population ID.
        policyIdentifier (str): The policy identifier.
        isCoupled (bool): Indicates if the policy is coupled.
        policyDescription (str): Description of the policy.
        economicCompensation (float): Economic compensation amount.
        modelLabel (Optional[str]): Label of the model.
        startYearNumber (int): Start year number.
        endYearNumber (int): End year number.
    """
    populationId: int
    policyIdentifier: str
    isCoupled: bool
    policyDescription: str
    economicCompensation: float
    modelLabel: Optional[str]
    startYearNumber: int
    endYearNumber: int

    
class PolicyGroupRelationJsonDTO(BaseModel):
    """
    DTO representing a policy group relation.

    Attributes:
        populationId (int): The population ID.
        policyIdentifier (str): The policy identifier.
        productGroupName (str): The name of the product group.
        economicCompensation (float): Economic compensation amount.
    """
    populationId: int
    policyIdentifier: str
    productGroupName: str
    economicCompensation: float
    
class ProductGroupJsonDTO(BaseModel):
    """
    DTO representing a product group.

    Attributes:
        name (str): The name of the product group.
        productType (str): Type of the product group.
        originalNameDatasource (str): Original name in the datasource.
        productsIncludedInOriginalDataset (str): Products included in the original dataset.
        modelSpecificCategories (List[str]): Model specific categories.
        organic (OrganicProductionType): Type of organic production.
        fadnProducts (List[FADNProductJsonDTO]): List of FADN products.
    """
    name: str
    productType: str
    originalNameDatasource: str
    productsIncludedInOriginalDataset: str
    modelSpecificCategories: List[str]
    organic: OrganicProductionType
    fadnProducts: List[FADNProductJsonDTO]
    
class LandRentJsonDTO(BaseModel):
    """
    DTO representing land rent information.

    Attributes:
        yearNumber (int): The year number.
        originFarmCode (str): The origin farm code.
        destinationFarmCode (str): The destination farm code.
        rentValue (float): The total rent price in euros.
        rentArea (float): The total rent area in hectares.
    """
    yearNumber: int
    originFarmCode: str
    destinationFarmCode: str
    # Total Rent Price [€]
    rentValue: float
    # Total Rent Area [ha]
    rentArea: float
    
class LandRentDTO(BaseModel):
    """
    DTO representing land rent details.

    Attributes:
        yearId (int): The year ID.
        originFarmId (int): The origin farm ID.
        destinationFarmId (int): The destination farm ID.
        rentValue (float): The total rent price in euros.
        rentArea (float): The total rent area in hectares.
    """
    yearId: int
    originFarmId: int
    destinationFarmId: int
    # Total Rent Price [€]
    rentValue: float
    # Total Rent Area [ha]
    rentArea: float