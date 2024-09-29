from pydantic import BaseModel
from typing import Optional, List
from enum import IntEnum
from agricore_sp_models.common_models import OrganicProductionType, ProductGroupJsonDTO, LandRentJsonDTO, LandRentDTO, PolicyJsonDTO, PolicyGroupRelationJsonDTO
from pydantic import confloat
    
class AgriculturalProduction(BaseModel):
    """
    Represents the agricultural production of a farm in a specific year.

    Attributes:
        id (Optional[int]): Unique identifier for the agricultural production.
        farmId (int): Identifier for the farm.
        yearId (int): Identifier for the year.
        productGroupId (Optional[int]): Identifier for the product group.
        valueSales (float): Value of sales (PLV - [€]).
        quantitySold (float): Quantity of sold production ([tons]).
        quantityUsed (float): Quantity of used production ([tons]).
        cropProduction (float): Value of total production (PLT - [€]).
        irrigatedArea (float): Irrigated area (IA - [ha]).
        cultivatedArea (float): Cultivated area (UAA - [ha]).
        organicProductionType (OrganicProductionType): Type of organic production.
        variableCosts (float): Variable costs per produced unit (CV - [€/ton]).
        landValue (float): Land value (PVF - [€]).
        sellingPrice (float): Unit selling price (PVU - [€/unit]).
    """
    id: Optional[int] = None
    farmId: int
    yearId: int
    productGroupId: Optional[int] = None
    # Value of Sales (PLV - [€])
    valueSales: float
    # Quantity of Sold Production ([tons])
    quantitySold: float
    # Quantity of Used Production ([tons])
    quantityUsed: float
    # Value of total production (PLT - [€])
    cropProduction: float
    # Irrigated Area (IA - [ha])
    irrigatedArea: float
    # Cultivated Area (UAA - [ha])
    cultivatedArea: float
    organicProductionType: OrganicProductionType
    # Variable Costs per produced unit (CV - [€/ton])
    variableCosts: float
    # Land Value (PVF - [€])
    landValue: float
    # Unit selling price (PVU - [€/unit])
    sellingPrice: float
    
class AgriculturalProductionDTO(BaseModel):
    """
    DTO for agricultural production.

    Attributes:
        id (Optional[int]): Unique identifier for the agricultural production.
        farmId (int): Identifier for the farm.
        yearId (int): Identifier for the year.
        productGroupId (Optional[int]): Identifier for the product group.
        valueSales (float): Value of sales (PLV - [€]).
        quantitySold (float): Quantity of sold production ([tons]).
        quantityUsed (float): Quantity of used production ([tons]).
        cropProduction (float): Value of total production (PLT - [€]).
        irrigatedArea (float): Irrigated area (IA - [ha]).
        cultivatedArea (float): Cultivated area (UAA - [ha]).
        organicProductionType (OrganicProductionType): Type of organic production.
        variableCosts (float): Variable costs per produced unit (CV - [€/ton]).
        landValue (float): Land value (PVF - [€]).
        sellingPrice (float): Unit selling price (PVU - [€/unit]).
    """

    id: Optional[int] = None
    farmId: int
    yearId: int
    productGroupId: Optional[int] = None
    # Value of Sales (PLV - [€])
    valueSales: float
    # Quantity of Sold Production ([tons])
    quantitySold: float
    # Quantity of Used Production ([tons])
    quantityUsed: float
    # Value of total production (PLT - [€])
    cropProduction: float
    # Irrigated Area (IA - [ha])
    irrigatedArea: float
    # Cultivated Area (UAA - [ha])
    cultivatedArea: float
    organicProductionType: OrganicProductionType
    # Variable Costs per produced unit (CV - [€/ton])
    variableCosts: float
    # Land Value (PVF - [€])
    landValue: float
    # Unit selling price (PVU - [€/unit])
    sellingPrice: float
    
class LivestockProduction(BaseModel):
    
    """
    Represents the livestock production of a farm in a specific year.

    Attributes:
        id (Optional[int]): Unique identifier for the livestock production.
        farmId (int): Identifier for the farm.
        yearId (int): Identifier for the year.
        productGroupId (Optional[int]): Identifier for the product group.
        numberOfAnimals (float): Number of animals [units].
        numberOfAnimalsSold (int): Number of animals sold [units].
        valueSoldAnimals (float): Value of sold animals ([€]).
        numberAnimalsForSlaughtering (int): Number of animals for slaughtering [units].
        valueSlaughteredAnimals (float): Value of slaughtered animals ([€]).
        numberAnimalsRearingBreading (float): Number of animals for rearing/breeding [units].
        valueAnimalsRearingBreading (float): Value of animals for rearing/breeding ([€]).
        milkTotalProduction (float): Total milk production [tons].
        milkProductionSold (float): Milk production sold [tons].
        milkTotalSales (float): Value of sold milk ([€]).
        milkVariableCosts (float): Variable costs per produced unit of milk (CV - [€/ton]).
        woolTotalProduction (float): Total wool production [tons].
        woolProductionSold (float): Wool production sold [tons].
        eggsTotalSales (float): Total sales of eggs ([€]).
        eggsTotalProduction (float): Total egg production [units].
        eggsProductionSold (float): Egg production sold [units].
        manureTotalSales (float): Total sales of manure ([€]).
        dairyCows (int): Number of dairy cows [UBA - [units]].
        variableCosts (float): Average variable costs per unit of product [€/ton].
    """
    id: Optional[int] = None
    farmId: int
    yearId: int
    productGroupId: Optional[int] = None
    # Number of Animals [units]
    numberOfAnimals: float
    # Number of Animals Sold [units]
    numberOfAnimalsSold: int
    # Value of Sold Animals ([€])
    valueSoldAnimals: float
    # Number of Animals for Slaughtering [units]
    numberAnimalsForSlaughtering: int
    # Value of Slaughtered Animals ([€])
    valueSlaughteredAnimals: float
    # Number of Animals for Rearing/Breading [units]
    numberAnimalsRearingBreading: float
    # Value of Animals Rearing/Breading ([€])
    valueAnimalsRearingBreading: float
    # Number of tons of milk produced [tons]
    milkTotalProduction: float
    # Number of tons of milk sold [tons]
    milkProductionSold: float
    # Value of Sold Milk ([€])
    milkTotalSales: float
    # Variable Costs per produced unit (CV - [€/ton])
    milkVariableCosts: float
    woolTotalProduction: float
    woolProductionSold: float
    eggsTotalSales: float
    eggsTotalProduction: float
    eggsProductionSold: float
    manureTotalSales: float
    # Number of dairy cows [UBA - [units]]
    dairyCows: int
    # Average variable cost per unit of product [€/ton]
    variableCosts: float

class Population(BaseModel):
    """
    Represents a population.

    Attributes:
        id (Optional[int]): Unique identifier for the population.
        description (str): Description of the population.
    """

    id: Optional[int] = None
    description: str

class SyntheticPopulation(BaseModel):
    
    """
    Represents a synthetic population.

    Attributes:
        id (Optional[int]): Unique identifier for the synthetic population.
        populationId (int): Identifier for the population.
        yearId (int): Identifier for the year.
        description (str): Description of the synthetic population.
        name (str): Name of the synthetic population.
    """
    id: Optional[int] = None
    populationId: int
    yearId: int
    description: str
    name: str
    
class Farm(BaseModel):

    """
    Represents a farm.

    Attributes:
        id (Optional[int]): Unique identifier for the farm.
        populationId (Optional[int]): Identifier for the population.
        lat (int): Latitude of the farm.
        long (int): Longitude of the farm.
        altitude (int): Altitude of the farm.
        regionLevel1 (str): Code for level 1 region.
        regionLevel1Name (str): Name of level 1 region.
        regionLevel2 (str): Code for level 2 region.
        regionLevel2Name (str): Name of level 2 region.
        regionLevel3 (int): Code for level 3 region.
        regionLevel3Name (str): Name of level 3 region.
        farmCode (str): Farm code.
        technicalEconomicOrientation (int): Technical-economic orientation.
        weight_ra (float): Weight relative to the region.
        weight_reg (float): Weight relative to the population.
    """
    id: Optional[int] = None
    populationId: Optional[int] = None
    lat: int
    long: int
    altitude: int
    regionLevel1: str
    regionLevel1Name: str
    regionLevel2: str
    regionLevel2Name: str
    regionLevel3: int
    regionLevel3Name: str
    farmCode: str
    technicalEconomicOrientation: int
    weight_ra: float
    weight_reg: float
        
class ProductGroup(BaseModel):
    """
    Represents a product group.

    Attributes:
        id (Optional[int]): Unique identifier for the product group.
        populationId (Optional[int]): Identifier for the population.
        name (str): Name of the product group.
        productType (int): Type of product.
        originalNameDatasource (str): Original name in the data source.
        productsIncludedInOriginalDataset (str): Products included in the original dataset.
        organic (OrganicProductionType): Type of organic production.
        modelSpecificCategories (List[str]): Model-specific categories.
    """
    id: Optional[int] = None
    populationId: Optional[int] = None
    name: str
    productType: int
    originalNameDatasource: str
    productsIncludedInOriginalDataset: str
    organic: OrganicProductionType
    modelSpecificCategories: List[str]
    
class FADNProductRelation(BaseModel):
    """
    Represents the relation between FADN products and product groups.

    Attributes:
        id (Optional[int]): Unique identifier for the FADN product relation.
        productGroupId (Optional[int]): Identifier for the product group.
        fadnProductId (Optional[int]): Identifier for the FADN product.
        populationId (Optional[int]): Identifier for the population.
    """
    id: Optional[int] = None
    productGroupId: Optional[int] = None
    fadnProductId: Optional[int] = None
    populationId: Optional[int] = None

class ClosingValue(BaseModel):

    """
    Represents the closing values for a farm in a specific year.

    Attributes:
        id (Optional[int]): Unique identifier for the closing value.
        agriculturalLandArea (float): Total area of agricultural land [ha].
        agriculturalLandValue (float): Total value of agricultural land [€].
        plantationsValue (float): Acquired agricultural land [ha].
        landImprovements (float): Investment in land improvements [€].
        forestLandArea (float): Total area of forest land [ha].
        forestLandValue (float): Total value of forest land [€].
        farmBuildingsValue (float): Value of buildings on the farm [€].
        machineryAndEquipment (float): Value of machinery and equipment on the farm [€].
        intangibleAssetsTradable (float): Value of tradable intangible assets [€].
        intangibleAssetsNonTradable (float): Value of non-tradable intangible assets [€].
        otherNonCurrentAssets (float): Value of other non-current assets [€].
        longAndMediumTermLoans (float): Total value of established long and medium term loans [€].
        totalCurrentAssets (float): Total value of current assets [€].
        farmNetIncome (float): Farm net income [€].
        grossFarmIncome (float): Gross farm income [€].
        subsidiesOnInvestments (float): Total value of subsidies on investments [€].
        vatBalanceOnInvestments (float): Balance of VAT on investments [€].
        totalOutputCropsAndCropProduction (float): Total value of agricultural production [€].
        totalOutputLivestockAndLivestockProduction (float): Total value of livestock production [€].
        otherOutputs (float): Total value of other outputs [€].
        totalIntermediateConsumption (float): Total value of intermediate consumption [€].
        taxes (float): Value of taxes [€].
        vatBalanceExcludingInvestments (float): Balance of VAT excluding investments [€].
        fixedAssets (float): Total value of fixed assets [€].
        depreciation (float): Yearly depreciation [€].
        totalExternalFactors (float): Total value of external factors [€].
        totalValueMachinery (float): Total value of machinery [€].
        farmId (int): Identifier for the farm.
        yearId (int): Identifier for the year.
    """
    id: Optional[int] = None
    # Total Area of type Agricultural Land [ha]
    agriculturalLandArea: float
    # Total value of Agricultural Land [€]
    agriculturalLandValue: float
    # Acquired Agricultural Land [ha]
    plantationsValue: float
    # Investment in Land improvements [€]
    landImprovements: float
    # Total Area of type Forest Land [ha]
    forestLandArea: float
    # Total value of Forest Land [€]
    forestLandValue: float
    # Value of Buildings in the farm [€]
    farmBuildingsValue: float
    # Value of Machinery and Equipment in the farm [€]
    machineryAndEquipment: float
    # Value of intangible assets that are tradable [€]
    intangibleAssetsTradable: float
    # Value of intangible assets that are non-tradable [€]
    intangibleAssetsNonTradable: float
    # Value of other non-current assets [€]
    otherNonCurrentAssets: float
    # Total value of established long and medium term loans [€]
    longAndMediumTermLoans: float
    # Total value of current assets [€]
    totalCurrentAssets: float
    # Farm Net Income [€]
    farmNetIncome: float
    # Gross Farm Income [€]
    grossFarmIncome: float
    # Total value of subsidies on investments [€]
    subsidiesOnInvestments: float
    # Balance of Taxes on Investments [€]
    vatBalanceOnInvestments: float
    # Total value of Agricultural Production [€]
    totalOutputCropsAndCropProduction: float
    # Total value of Livestock Production [€]
    totalOutputLivestockAndLivestockProduction: float
    # Total value of other outputs [€]
    otherOutputs: float
    # Total value of intermediate consumption [€]
    totalIntermediateConsumption: float
    # Value of Taxes (>0 received , <0 paid) [€]
    taxes: float
    # Balance of VAT excluding investments [€]
    vatBalanceExcludingInvestments: float
    # Total value of Fixed Assets [€]
    fixedAssets: float
    # Yearly Depreciation [€]
    depreciation: float
    # Total value of External Factors [€]
    totalExternalFactors: float
    # Total value of Machinery [€]
    machinery: float
    farmId: int
    yearId: int
    
class Policy(BaseModel):
    """
    Represents a policy with economic compensation and its attributes.

    Attributes:
        id (Optional[int]): Unique identifier for the policy.
        policyIdentifier (str): Identifier for the policy.
        policyDescription (str): Description of the policy.
        economicCompensation (float): Economic compensation for the policy.
        isCoupled (bool): Indicates if the policy is coupled.
    """
    id: Optional[int] = None
    policyIdentifier: str
    policyDescription: str
    # Economic compensation for the policy. For the coupled ones, this values is a rate to be multiplied by the ha of the associated crops
    # The compensation is weighted in relation with the original distribution of the crops in the original population
    economicCompensation:float
    isCoupled: bool
    
class PolicyProductGroupRelation(BaseModel):
    
    """
    Represents the relation between policy and product groups.

    Attributes:
        id (Optional[int]): Unique identifier for the policy-product group relation.
        productGroupId (int): Identifier for the product group.
        policyId (int): Identifier for the policy.
        populationId (Optional[int]): Identifier for the population.
        economicCompensation (float): Economic compensation for the relation.
    """
    id: Optional[int] = None
    productGroupId: int
    policyId: int
    populationId: Optional[int] = None
    economicCompensation:float

class HolderFarmYearData(BaseModel):
    
    """
    Represents data related to the farm holder for a specific year.

    Attributes:
        id (Optional[int]): Unique identifier for the holder-farm-year data.
        farmId (Optional[int]): Identifier for the farm.
        yearId (Optional[int]): Identifier for the year.
        holderAge (int): Age of the holder.
        holderGender (int): Gender of the holder.
        holderSuccessors (int): Number of successors of the holder.
        holderSuccessorsAge (int): Age of the holder's successors.
        holderFamilyMembers (int): Number of family members of the holder.
    """
    id: Optional[int] = None
    farmId: Optional[int] = None
    yearId: Optional[int] = None
    holderAge: int
    holderGender: int
    holderSuccessors: int
    holderSuccessorsAge: int
    holderFamilyMembers: int
    
class FarmYearSubsidy(BaseModel):
    
    """
    Represents the subsidy received by a farm in a specific year.

    Attributes:
        id (Optional[int]): Unique identifier for the farm-year subsidy.
        farmId (int): Identifier for the farm.
        yearId (int): Identifier for the year.
        policyId (int): Identifier for the policy.
        value (float): Value of the subsidy.
    """
    id: Optional[int] = None
    farmId: int
    yearId: int
    policyId: int
    value: float

class FarmYearSubsidyDTO(BaseModel):
    """
    Data Transfer Object for farm-year subsidy details.

    Attributes:
        farmId (Optional[int]): Identifier for the farm.
        yearNumber (int): The year number.
        value (float): Value of the subsidy.
        policyIdentifier (str): Identifier for the policy.
    """
    farmId: Optional[int] = None
    yearNumber: int
    value: float
    policyIdentifier: str

class HolderInfoDTO(BaseModel):
    """
    Data Transfer Object for holder information.

    Attributes:
        holderAge (int): Age of the holder.
        holderSuccessorsAge (int): Age of the holder's successors.
        holderSuccessors (int): Number of successors of the holder.
        holderFamilyMembers (int): Number of family members of the holder.
        holderGender (str): Gender of the holder.
    """
    holderAge: int
    holderSuccessorsAge: int
    holderSuccessors: int
    holderFamilyMembers: int
    holderGender: str

class ValueToLPDTO(BaseModel):
    """
    Represents values to be sent to LP (Linear Programming) model.

    Attributes:
        farmId (int): Identifier for the farm.
        yearId (int): Identifier for the year.
        agriculturalLandValue (float): Value of agricultural land [€].
        agriculturalLandArea (float): Area of agricultural land [ha].
        sE465 (float): Current assets in SP model [€].
        sE490 (float): SE490 value [€].
        averageHAPrice (float): Average price per hectare [€/ha].
        sE420 (float): SE420 value [€].
        sE410 (float): SE410 value [€].
        aversionRiskFactor (float): Aversion risk factor.
        agentHolder (Optional[HolderInfoDTO]): Information about the agent holder.
        agentSubsidies (Optional[List[FarmYearSubsidyDTO]]): List of subsidies received by the agent.
        regionLevel3 (int): Identifier for the region level 3.
    """
    farmId: int
    yearId: int
    agriculturalLandValue: float
    agriculturalLandArea: float
    # CurrentAssets in SP model [€]
    sE465: float
    # SE490 [€]
    sE490: float
    # Average ha price [€/ha]
    averageHAPrice: float
    # SE420 [€]
    sE420: float
    # SE410 [€]
    sE410: float
    # Aversion risk factor [TBD]
    aversionRiskFactor: float
    agentHolder: Optional[HolderInfoDTO] = None
    agentSubsidies: Optional[List[FarmYearSubsidyDTO]] = None
    regionLevel3: int

class CropDataDTO(BaseModel):
    """
    Data Transfer Object for crop data.

    Attributes:
        cropProductiveArea (float): Productive area of the crop [ha].
        cropVariableCosts (float): Variable costs per produced unit [€/ton].
        quantitySold (float): Quantity of sold production [tons].
        quantityUsed (float): Quantity of used production [tons].
        cropSellingPrice (float): Unit selling price [€/unit].
        coupledSubsidy (float): Total value of coupled subsidy received [€].
        uaa (float): Used area [ha].
        rebreedingCows (float): Number of rebreeding cows [LSU].
        dairyCows (float): Number of dairy cows [LSU].
    """
    # Crop productive Area [ha]
    cropProductiveArea: float
    # Variable Costs per produced unit (CV - [€/ton])
    cropVariableCosts: float
    # Quantity of Sold Production ([tons])
    quantitySold: float
    # Quantity of Used Production ([tons])
    quantityUsed: float
    # Unit selling price (PVU - [€/unit])
    cropSellingPrice: float
    # Total value of coupled subsidy received [€]
    coupledSubsidy: float
    # Used Area [ha]
    uaa: float
    # Number (LSU) of rebreeding cows
    rebreedingCows: float
    # Number (LSU) of dairy cows
    dairyCows: float

class ValueFromSPDTO(BaseModel):
    """
    Represents values received from SP (Stochastic Programming) model.

    Attributes:
        farmId (int): Identifier for the farm.
        totalCurrentAssets (float): Total current assets [€].
        farmNetIncome (float): Farm net income [€].
        farmGrossIncome (float): Gross farm income [€].
        agriculturalLand (float): Area of agricultural land [ha].
        crops (dict[str, CropDataDTO]): Dictionary of crop data.
        totalVariableCosts (float): Total variable costs [€].
        rentBalanceArea (float): Balance of the rented area [ha].
        greeningSurface (float): Greening surface [ha].
        rentedInLands (List[LandRentDTO]): List of rented in lands.
        subsidies (List[FarmYearSubsidyDTO]): List of subsidies received by the farm.
    """
    farmId: int
    # Total Current Assets [€]
    totalCurrentAssets: float
    # Farm Net Income [€]
    farmNetIncome: float
    # Gross Farm Income [€]
    farmGrossIncome: float
    # Area of Agricultural Land [ha]
    agriculturalLand: float
    crops: dict[str,CropDataDTO]
    # Total Variable Costs [€]
    totalVariableCosts: float
    # Balance of the rented area (>0 if the farmer is renting in land) [ha]
    rentBalanceArea: float
    # Greening Surface [ha]
    greeningSurface: float
    # Land rents where the destination farm is this one
    rentedInLands: List[LandRentDTO]
    # Subsidies received by the farm
    subsidies: List[FarmYearSubsidyDTO]

class LivestockDTO(BaseModel):
    """
    Data Transfer Object for livestock data.

    Attributes:
        numberOfAnimals (float): Number of animals [units].
        dairyCows (int): Number of dairy cows [units].
        rebreedingCows (float): Number of rebreeding cows [units].
        milkProduction (float): Quantity of produced milk [tons].
        milkSellingPrice (float): Unit value of sold milk [€/ton].
        variableCosts (float): Variable costs per produced unit [€/ton].
    """
    # Number of animals [units]
    numberOfAnimals: float
    # Number of dairy cows [units]
    dairyCows: int
    # Number of rebreeding cows [units]
    rebreedingCows: float
    # Quantity of produced milk [tons]
    milkProduction: float
    # Unit value of sold milk [€/ton]
    milkSellingPrice: float
    # Variable costs per produced unit (CV - [€/ton])
    variableCosts: float

class AltitudeEnum(IntEnum):
    """
    Enumeration for altitude categories.

    Attributes:
        MOUNTAINS (int): Represents mountainous areas.
        HILLS (int): Represents hilly areas.
        PLAINS (int): Represents plains.
    """
    MOUNTAINS = 1
    HILLS = 2
    PLAINS = 3

class ValueToSPDTO(BaseModel):
    """
    Represents values to be sent to SP (Stochastic Programming) model.

    Attributes:
        farmCode (int): Code of the farm.
        holderInfo (Optional[HolderInfoDTO]): Information about the farm holder.
        cod_RAGR (str): RAGR code.
        cod_RAGR2 (str): RAGR2 code.
        cod_RAGR3 (int): RAGR3 code.
        technicalEconomicOrientation (int): Technical economic orientation.
        altitude (AltitudeEnum): Altitude category.
        currentAssets (float): Current assets [€].
        crops (dict[str, CropDataDTO]): Dictionary of crop data.
        livestock (Optional[LivestockDTO]): Livestock data.
        greeningSurface (float): Greening surface [ha].
        rentedInLands (List[LandRentDTO]): List of rented in lands.
    """
    farmCode: int
    holderInfo: Optional[HolderInfoDTO] = None
    cod_RAGR: str
    cod_RAGR2: str
    cod_RAGR3: int
    technicalEconomicOrientation: int
    altitude: AltitudeEnum
    currentAssets: float
    crops: dict[str,CropDataDTO]
    livestock: Optional[LivestockDTO] = None
    # Greening Surface [ha]
    greeningSurface: float
    rentedInLands: List[LandRentDTO]

class DataToSPDTO(BaseModel):
    """
    Represents data to be sent to SP (Stochastic Programming) model.

    Attributes:
        values (List[ValueToSPDTO]): List of values to be sent.
        productGroups (List[ProductGroupJsonDTO]): List of product groups.
        policies (List[PolicyJsonDTO]): List of policies.
        policyGroupRelations (List[PolicyGroupRelationJsonDTO]): List of policy group relations.
        farmYearSubsidies (List[FarmYearSubsidyDTO]): List of farm-year subsidies.
    """
    values: List[ValueToSPDTO]
    productGroups: List[ProductGroupJsonDTO]
    policies: List[PolicyJsonDTO]
    policyGroupRelations: List[PolicyGroupRelationJsonDTO]
    farmYearSubsidies: List[FarmYearSubsidyDTO]

class IntermediateValueFromLP(BaseModel):
    
    """
    Represents intermediate values received from LP (Linear Programming) model.

    Attributes:
        farmId (int): Identifier for the farm.
        averageHAPrice (float): Average price per hectare.
        previousAgriculturalLand (float): Previous agricultural land area.
        result (dict): Result dictionary.
    """
    farmId: int
    averageHAPrice: float
    previousAgriculturalLand: float
    result: dict

class LandTransaction(BaseModel):
    """
    Represents a land transaction between farms.

    Attributes:
        productionId (int): Identifier for the production.
        destinationFarmId (int): Identifier for the destination farm.
        yearId (int): Identifier for the year.
        percentage (confloat(ge=0, le=1)): Percentage of the land transaction.
        salePrice (float): Sale price of the land.
    """
    productionId: int
    destinationFarmId: int
    yearId: int
    percentage: confloat(ge=0, le=1)
    salePrice: float

class AgroManagementDecisions(BaseModel):
    
    """
    Represents agro-management decisions made by a farm.

    Attributes:
        farmId (int): Identifier for the farm.
        yearId (int): Identifier for the year.
        agriculturalLandArea (float): Total area of agricultural land [ha].
        agriculturalLandValue (float): Total value of agricultural land [€].
        longAndMediumTermLoans (float): Amount of established long and medium term loans [€].
        totalCurrentAssets (float): Total current assets [€].
        averageLandValue (float): Average hectare price of the owned land [€/ha].
        targetedLandAquisitionArea (float): Total amount of land the farmer is willing to acquire [ha].
        targetedLandAquisitionHectarPrice (float): Price per hectare the farmer is willing to pay for the land [€/ha].
        retireAndHandOver (bool): Indicates if the farmer is willing to retire and hand over the farm to successors.
    """
    farmId: int
    yearId: int
    # Total Area of type Agricultural Land [ha]
    agriculturalLandArea: float
    # Total Value of type Agricultural Land [ha]
    agriculturalLandValue: float
    # Amount of stablished loans at long and medium term [€]
    longAndMediumTermLoans: float
    # Total current assets [€]
    totalCurrentAssets: float
    # Average hectar price of the owned land [€/ha]
    averageLandValue: float
    # Total amount of land the farmer is willing to acquire [ha]
    targetedLandAquisitionArea: float
    # Price per hectar the farmer is willing to pay for the land [€/ha]
    targetedLandAquisitionHectarPrice: float
    # Boolean to indicate if the farmer is willing to retire and hand over the farm to its successors
    retireAndHandOver: bool

class AgroManagementDecisionFromLP(BaseModel):
    """
    Represents agro-management decisions received from LP (Linear Programming) model.

    Attributes:
        agroManagementDecisions (List[AgroManagementDecisions]): List of agro-management decisions.
        landTransactions (List[LandTransaction]): List of land transactions.
        errorList (List[int]): List of errors.
    """
    agroManagementDecisions: List[AgroManagementDecisions]
    landTransactions: List[LandTransaction]
    errorList: List[int]

class DataToLPDTO(BaseModel):
    """
    Represents data to be sent to LP (Linear Programming) model.

    Attributes:
        values (List[ValueToLPDTO]): List of values to be sent.
        agriculturalProductions (List[AgriculturalProductionDTO]): List of agricultural productions.
        policyGroupRelations (List[PolicyGroupRelationJsonDTO]): List of policy group relations.
        ignoreLP (Optional[bool]): Flag to ignore LP.
        ignoreLMM (Optional[bool]): Flag to ignore LMM.
        policies (Optional[List[PolicyJsonDTO]]): List of policies.
        rentOperations (Optional[List[LandRentDTO]]): List of rent operations.
    """
    values: List[ValueToLPDTO]
    agriculturalProductions: List[AgriculturalProductionDTO]
    policyGroupRelations: List[PolicyGroupRelationJsonDTO]
    ignoreLP: Optional[bool]
    ignoreLMM: Optional[bool]
    policies: Optional[List[PolicyJsonDTO]]
    rentOperations: Optional[List[LandRentDTO]]

