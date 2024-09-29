from pydantic import BaseModel
from typing import Optional, Any, List
from enum import IntEnum

class SimulationStage(IntEnum):
    """
    Enum representing the different stages of a simulation.

    Attributes:
        DATAPREPARATION (int): Data preparation stage.
        LONGPERIOD (int): Long period stage.
        LANDMARKET (int): Land market stage.
        CALIBRATION (int): Calibration stage.
        SHORTPERIOD (int): Short period stage.
        REALISATION (int): Realisation stage.
    """
    DATAPREPARATION = 1
    LONGPERIOD = 2
    LANDMARKET = 3
    CALIBRATION = 4
    SHORTPERIOD = 5
    REALISATION = 6
    
class CoupledCompensationForUIDTO(BaseModel):
    """
    DTO representing coupled compensation for a UI.

    Attributes:
        productGroup (str): The product group.
        economicCompensation (float): The economic compensation amount.
    """
    productGroup: str
    economicCompensation: float
    
class PolicyForUIDTO(BaseModel):
    """
    DTO representing a policy for a UI.

    Attributes:
        populationId (int): The population ID.
        policyIdentifier (str): The policy identifier.
        isCoupled (bool): Indicates if the policy is coupled.
        policyDescription (str): Description of the policy.
        economicCompensation (float): Economic compensation amount.
        modelLabel (str): Label of the model.
        startYearNumber (int): Start year number.
        endYearNumber (int): End year number.
        coupledCompensations (Optional[List[CoupledCompensationForUIDTO]]): List of coupled compensations.
    """
    populationId: int
    policyIdentifier: str
    isCoupled: bool
    policyDescription: str
    economicCompensation: float
    modelLabel: str
    startYearNumber: int
    endYearNumber: int
    coupledCompensations: Optional[List[CoupledCompensationForUIDTO]] = None
    
class SimulationScenario(BaseModel):
    """
    Model representing a simulation scenario.

    Attributes:
        id (Optional[int]): The ID of the simulation scenario.
        populationId (int): The population ID.
        yearId (int): The year ID.
        ignoreLP (Optional[bool]): Indicates if LP should be ignored.
        ignoreLMM (Optional[bool]): Indicates if LMM should be ignored.
        compress (Optional[bool]): Indicates if compression should be applied.
        yearToContinueFrom (Optional[int]): The year to continue from.
        stageToContinueFrom (Optional[SimulationStage]): The stage to continue from.
        shortTermModelBranch (str): The short-term model branch.
        longTermModelBranch (str): The long-term model branch.
        horizon (int): The horizon.
        queueSuffix (Optional[str]): The queue suffix.
        additionalPolicies (Optional[List[PolicyForUIDTO]]): List of additional policies.
    """
    id: Optional[int] = None
    populationId: int
    yearId: int
    ignoreLP: Optional[bool]
    ignoreLMM: Optional[bool]
    compress: Optional[bool] = False
    yearToContinueFrom: Optional[int] = None
    stageToContinueFrom: Optional[SimulationStage] = None
    shortTermModelBranch: str
    longTermModelBranch: str
    horizon: int
    queueSuffix: Optional[str] = None
    additionalPolicies: Optional[List[PolicyForUIDTO]] = None

class LogLevel(IntEnum):
    """
    Enum representing the log levels.

    Attributes:
        TRACE (int): Trace level.
        DEBUG (int): Debug level.
        INFO (int): Info level.
        SUCCESS (int): Success level.
        WARNING (int): Warning level.
        ERROR (int): Error level.
        CRITICAL (int): Critical level.
    """
    TRACE = 5
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class LogMessage(BaseModel):
    """
    Model representing a log message.

    Attributes:
        simulationRunId (int): The ID of the simulation run.
        timestamp (int): The timestamp of the log message.
        source (str): The source of the log message.
        logLevel (LogLevel): The log level.
        title (str): The title of the log message.
        description (str): The description of the log message.
    """
    simulationRunId: int
    timestamp: int
    source: str
    logLevel: LogLevel
    title: str
    description: str

class OverallStatus(IntEnum):
    """
    Enum representing the overall status of a simulation run.

    Attributes:
        INPROGRESS (int): In progress status.
        CANCELLED (int): Cancelled status.
        COMPLETED (int): Completed status.
        ERROR (int): Error status.
    """
    INPROGRESS = 1
    CANCELLED = 2
    COMPLETED = 3
    ERROR = 4
    
class SimulationRun(BaseModel):
    """
    Model representing a simulation run.

    Attributes:
        id (Optional[int]): The ID of the simulation run.
        simulationScenarioId (int): The ID of the simulation scenario.
        logMessages (Optional[List[LogMessage]]): List of log messages.
        overallStatus (OverallStatus): The overall status.
        currentStage (SimulationStage): The current stage.
        currentYear (int): The current year.
        currentSubstage (str): The current substage.
        currentStageProgress (int): The progress of the current stage.
        currentSubStageProgress (int): The progress of the current substage.
    """
    id: Optional[int] = None
    simulationScenarioId: int
    logMessages: Optional[List[LogMessage]] = None
    overallStatus: OverallStatus
    currentStage: SimulationStage
    currentYear: int
    currentSubstage: str
    currentStageProgress: int
    currentSubStageProgress: int
