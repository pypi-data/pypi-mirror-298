from agricore_sp_models.common_models import OrganicProductionType, PolicyJsonDTO, ProductGroupJsonDTO, LandRentJsonDTO, PolicyGroupRelationJsonDTO
from pydantic import BaseModel, Field
from typing import List

class AgriculturalProductionJsonDTO(BaseModel):
    """
    Data Transfer Object for agricultural production details.

    Attributes:
        yearNumber (int): The year number of the production.
        productName (str): Name of the product.
        organicProductionType (OrganicProductionType): Type of organic production.
        cultivatedArea (float): Utilized Agricultural Area (UAA) in hectares [ha].
        irrigatedArea (float): Irrigated Area (IA) in hectares [ha].
        cropProduction (float): Value of total production in euros [€].
        quantitySold (float): Quantity of sold production in tons [tons].
        quantityUsed (float): Quantity of used production in tons [tons].
        valueSales (float): Value of sales in euros [€].
        variableCosts (float): Variable costs per produced unit in euros per ton [€/ton].
        landValue (float): Value of the land in euros [€].
        sellingPrice (float): Unit selling price in euros per unit [€/unit].
    """
    yearNumber: int
    productName: str 
    organicProductionType: OrganicProductionType
    # Utilized Agricultural Area (UAA - [ha])
    cultivatedArea: float
    # Irrigated Area (IA - [ha])
    irrigatedArea: float 
    # Value of total production (PLT - [€])
    cropProduction: float
    # Quantity of Sold Production ([tons])
    quantitySold: float
    # Quantity of Used Production ([tons])
    quantityUsed: float
    # Value of Sales (PLV - [€])
    valueSales: float 
    # Variable Costs per produced unit (CV - [€/ton])
    variableCosts: float 
    # Land Value (PVF - [€])
    landValue: float 
    # Unit selling price (PVU - [€/unit])
    sellingPrice: float

class LivestockProductionJsonDTO(BaseModel):
    """
    Data Transfer Object for livestock production details.

    Attributes:
        yearNumber (int): The year number of the production.
        productName (str): Name of the product.
        numberOfAnimals (float): Number of animals in units [units].
        dairyCows (int): Number of dairy cows in units [UBA - units].
        numberOfAnimalsSold (int): Number of animals sold in units [units].
        valueSoldAnimals (float): Value of sold animals in euros [€].
        numberAnimalsForSlaughtering (int): Number of animals for slaughtering in units [units].
        valueSlaughteredAnimals (float): Value of slaughtered animals in euros [€].
        numberAnimalsRearingBreading (float): Number of animals for rearing/breeding in units [units].
        valueAnimalsRearingBreading (float): Value of animals for rearing/breeding in euros [€].
        milkTotalProduction (float): Number of tons of milk produced in tons [tons].
        milkProductionSold (float): Number of tons of milk sold in tons [tons].
        milkTotalSales (float): Value of milk sold in euros [€].
        milkVariableCosts (float): Variable costs per produced unit of milk in euros per ton [€/ton].
        woolTotalProduction (float): Total production of wool.
        woolProductionSold (float): Production of wool sold.
        eggsTotalSales (float): Total sales of eggs.
        eggsTotalProduction (float): Total production of eggs.
        eggsProductionSold (float): Production of eggs sold.
        manureTotalSales (float): Total sales of manure.
        variableCosts (float): Average variable cost per unit of product in euros per ton [€/ton].
        sellingPrice (float): Average selling price per unit of product in euros per ton [€/ton].
    """
    yearNumber: int
    productName: str
    # Number of Animals [units]
    numberOfAnimals: float
    # Number of dairy cows [UBA - [units]]
    dairyCows: int
    # Number of Animals Sold [units]
    numberOfAnimalsSold: int
    # Value of Sold Animals ([€])
    valueSoldAnimals: float
    # Number of Animals for Slaughtering [units]
    numberAnimalsForSlaughtering: int
    # Value of Slaughtered Animals ([€])
    valueSlaughteredAnimals: float
    # Number of Animals for Rearing/Breeding [units]
    numberAnimalsRearingBreading: float
    # Value of Animals for Rearing/Breeding ([€])
    valueAnimalsRearingBreading: float
    # Number of tons of milk produced [tons]
    milkTotalProduction: float
    # Number of tons of milk sold [tons]
    milkProductionSold: float
    # Value of milk sold ([€])
    milkTotalSales: float
    # Variable Costs per produced unit (CV - [€/ton])
    milkVariableCosts: float
    woolTotalProduction: float
    woolProductionSold: float
    eggsTotalSales: float
    eggsTotalProduction: float
    eggsProductionSold: float
    manureTotalSales: float
    # Average variable cost per unit of product[€/ ton]
    variableCosts: float
    # Average sell price per unit of product[€/ ton]
    sellingPrice: float
    
class HolderFarmYearDataJsonDTO(BaseModel):
    """
    Data Transfer Object for holder farm year data details.

    Attributes:
        yearNumber (int): The year number.
        holderAge (int): Age of the holder.
        holderFamilyMembers (int): Number of family members of the holder.
        holderSuccessorsAge (int): Age of the holder's successors.
        holderGender (str): Gender of the holder.
        holderSuccessors (int): Number of successors of the holder.
    """
    yearNumber: int
    holderAge: int
    holderFamilyMembers: int
    holderSuccessorsAge: int
    holderGender: str
    holderSuccessors: int
    
class ClosingValFarmValueDTO(BaseModel):
    
    """
    Represents the closing value of farm assets.

    Attributes:
        agriculturalLandArea (float): Total area of agricultural land in hectares [ha].
        agriculturalLandValue (float): Total value of agricultural land in euros [€].
        agriculturalLandHectaresAdquisition (float): Acquired agricultural land in hectares [ha].
        landImprovements (float): Investment in land improvements in euros [€].
        forestLandArea (float): Total area of forest land in hectares [ha].
        forestLandValue (float): Total value of forest land in euros [€].
        farmBuildingsValue (float): Value of buildings on the farm in euros [€].
        machineryAndEquipment (float): Value of machinery and equipment on the farm in euros [€].
        intangibleAssetsTradable (float): Value of tradable intangible assets in euros [€].
        intangibleAssetsNonTradable (float): Value of non-tradable intangible assets in euros [€].
        otherNonCurrentAssets (float): Value of other non-current assets in euros [€].
        longAndMediumTermLoans (float): Total value of established long and medium-term loans in euros [€].
        totalCurrentAssets (float): Total value of current assets in euros [€].
        farmNetIncome (float): Farm net income in euros [€].
        grossFarmIncome (float): Gross farm income in euros [€].
        subsidiesOnInvestments (float): Total value of subsidies on investments in euros [€].
        vatBalanceOnInvestments (float): Balance of VAT on investments in euros [€].
        totalOutputCropsAndCropProduction (float): Total value of agricultural production in euros [€].
        totalOutputLivestockAndLivestockProduction (float): Total value of livestock production in euros [€].
        otherOutputs (float): Total value of other outputs in euros [€].
        totalIntermediateConsumption (float): Total value of intermediate consumption in euros [€].
        taxes (float): Value of taxes in euros (positive if received, negative if paid) [€].
        vatBalanceExcludingInvestments (float): Balance of VAT excluding investments in euros [€].
        fixedAssets (float): Total value of fixed assets in euros [€].
        depreciation (float): Yearly depreciation in euros [€].
        totalExternalFactors (float): Total value of external factors in euros [€].
        machinery (float): Total value of machinery in euros [€].
        yearNumber (int): The year number.
        rentBalance (float): Balance of rent operations in euros (positive if received, negative if paid) [€].
    """
    # Total Area of type Agricultural Land [ha]
    agriculturalLandArea: float
    # Total value of Agricultural Land [€]
    agriculturalLandValue: float
    # Acquired Agricultural Land [ha]
    agriculturalLandHectaresAdquisition: float
    # Invesment in Land improvements [€]
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
    yearNumber: int
    # Balance (>0 received , <0 paid) of rent operations [€]
    rentBalance: float

class FarmYearSubsidyDTO(BaseModel):
    """
    Data Transfer Object for farm year subsidy details.

    Attributes:
        yearNumber (int): The year number.
        value (float): Value of the subsidy in euros [€].
        policyIdentifier (str): Identifier for the policy.
    """
    yearNumber: int
    value: float
    policyIdentifier: str
    
class LandTransactionJsonDTO(BaseModel):
    """
    Represents a land transaction between farms.

    Attributes:
        yearNumber (int): The year number.
        productGroupName (str): Name of the product group.
        destinationFarmCode (str): Code of the destination farm.
        originFarmCode (str): Code of the origin farm.
        percentage (float): Percentage of the land transferred from the origin farm to the destination farm in the range [0,1].
        salePrice (float): Sale price of the land transferred from the origin farm to the destination farm in euros [€].
    """
    yearNumber: int
    productGroupName: str
    destinationFarmCode: str
    originFarmCode: str
    # Percentage of the land transferred from the origin farm to the destination farm in [0,1] range
    percentage: float = Field(..., ge=0, le=1)
    # Sale price of the land transferred from the origin farm to the destination farm [€]
    salePrice: float
    
class GreeningFarmYearDataJsonDTO(BaseModel):
    """
    Data Transfer Object for greening farm year data details.

    Attributes:
        yearNumber (int): The year number.
        greeningSurface (float): Greening surface in hectares [ha].
    """
    yearNumber: int
    # Greening Surface [ha]
    greeningSurface: float
    
class FarmJsonDTO(BaseModel):
    """
    Represents a farm with its associated data.

    Attributes:
        farmCode (str): Code of the farm.
        lat (int): Latitude of the farm.
        long (int): Longitude of the farm.
        altitude (str): Altitude of the farm.
        regionLevel1 (str): Level 1 region code.
        regionLevel1Name (str): Level 1 region name.
        regionLevel2 (str): Level 2 region code.
        regionLevel2Name (str): Level 2 region name.
        regionLevel3 (str): Level 3 region code.
        regionLevel3Name (str): Level 3 region name.
        technicalEconomicOrientation (int): Technical economic orientation.
        agriculturalProductions (List[AgriculturalProductionJsonDTO]): List of agricultural productions.
        livestockProductions (List[LivestockProductionJsonDTO]): List of livestock productions.
        holderFarmYearsData (List[HolderFarmYearDataJsonDTO]): List of holder farm year data.
        closingValFarmValues (List[ClosingValFarmValueDTO]): List of closing values of farm assets.
        farmYearSubsidies (List[FarmYearSubsidyDTO]): List of farm year subsidies.
        greeningFarmYearData (List[GreeningFarmYearDataJsonDTO]): List of greening farm year data.
    """
    farmCode: str
    lat: int
    long: int
    altitude: str = ""
    regionLevel1: str
    regionLevel1Name: str = ""
    regionLevel2: str
    regionLevel2Name: str = ""
    regionLevel3: str
    regionLevel3Name: str = ""
    technicalEconomicOrientation: int
    agriculturalProductions: List[AgriculturalProductionJsonDTO]
    livestockProductions: List[LivestockProductionJsonDTO]
    holderFarmYearsData: List[HolderFarmYearDataJsonDTO]
    closingValFarmValues: List[ClosingValFarmValueDTO]
    farmYearSubsidies: List[FarmYearSubsidyDTO]
    greeningFarmYearData: List[GreeningFarmYearDataJsonDTO]
    
class PopulationJsonDTO(BaseModel):
    """
    Represents a population of farms with associated data.

    Attributes:
        description (str): Description of the population.
        farms (List[FarmJsonDTO]): List of farms.
        productGroups (List[ProductGroupJsonDTO]): List of product groups.
        policies (List[PolicyJsonDTO]): List of policies.
        landTransactions (List[LandTransactionJsonDTO]): List of land transactions.
        landRents (List[LandRentJsonDTO]): List of land rents.
        policyGroupRelations (List[PolicyGroupRelationJsonDTO]): List of policy group relations.
    """
    description: str = ""
    farms: List[FarmJsonDTO]
    productGroups: List[ProductGroupJsonDTO]
    policies: List[PolicyJsonDTO]
    landTransactions: List[LandTransactionJsonDTO]
    landRents: List[LandRentJsonDTO]
    policyGroupRelations: List[PolicyGroupRelationJsonDTO]

class SyntheticPopulationJsonDTO(BaseModel):
    """
    Represents a synthetic population with associated data.

    Attributes:
        description (str): Description of the synthetic population.
        name (str): Name of the synthetic population.
        yearNumber (int): The year number.
        population (PopulationJsonDTO): The population data.
    """
    description: str = ""
    name: str = ""
    yearNumber: int
    population: PopulationJsonDTO