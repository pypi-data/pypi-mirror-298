from __future__ import annotations
from loguru import logger
from .simulation_models import LogLevel, LogMessage
from time import time
from urllib.parse import urljoin
import json
import requests

class ORMLogHandler:
    """
    A handler for sending log messages to an ORM (Object-Relational Mapper) system.

    Attributes:
        base_path (str): The base URL path for the ORM system. Default is "https://abm.agricore.idener.es/".
        headers (dict): HTTP headers used for sending requests.

    Methods:
        __init__(base_path: str = "https://abm.agricore.idener.es/") -> None:
            Initializes the ORMLogHandler with a base path URL.

        write(message: LogMessage) -> None:
            Sends a log message to the ORM system.

    """
    def __init__(self, base_path: str = "https://abm.agricore.idener.es/"):
        """
        Initializes the ORMLogHandler with a base path URL.

        Parameters:
            base_path (str): The base URL path for the ORM system. Default is "https://abm.agricore.idener.es/".
        
        Returns:
            None
        """
        self.base_path = base_path
        self.headers = {'Accept': 'text/plain', 'Content-Type': 'application/json'}
        
    def write(self, message):
        """
        Sends a log message to the ORM system.

        Parameters:
            message (LogMessage): The log message to be sent. The `LogMessage` object should include fields such as
                                  description, logLevel, simulationRunId, source, timestamp, and title.

        Returns:
            None
        
        Raises:
            Exception: If there is an issue with sending the log message to the ORM system.
        """
        try:
            log = LogMessage(
                description="" if message.record["exception"] is None else str(message.record["exception"]),
                logLevel=int(message.record["level"].no),
                simulationRunId=0 if "simulationRunId" not in message.record["extra"] else message.record["extra"]["simulationRunId"],
                source="" if "logSource" not in message.record["extra"] else message.record["extra"]["logSource"],
                timestamp=float(time() * 1000),
                title=message.record["message"],
            )
            url = urljoin(self.base_path, f"/simulationRun/{log.simulationRunId}/logMessage/add")
            x = requests.post(url, json.dumps(log.dict(exclude={"id"})), headers= self.headers)
            if x.status_code == 415:
                logger.debug(f"The log message could not be added to the ORM. Object sent: {log.dict()}") 
                     
        except Exception as e:
            print("Unable to generate Log Message in ORM for message. " + str(e) )
            if log is not None:
                print (log.dict())
                
def check_orm_log(record):
    """
    Checks if the log record has the necessary fields to be processed by ORMLogHandler.

    Parameters:
        record (dict): The log record containing extra information.

    Returns:
        bool: True if the record contains both "simulationRunId" and "logSource" in its extra fields; False otherwise.
    """
    if "simulationRunId" in record["extra"] and "logSource" in record["extra"]:
        return True
    else:
        return False

def configure_orm_logger(url: str, enqueue: bool = True) -> None:
    """
    Configures the logger to use ORMLogHandler.

    Parameters:
        url (str): The base URL path for the ORM system.
        enqueue (bool): If True, log messages will be enqueued; if False, they will be processed synchronously.

    Returns:
        None
    """
    logger.configure(handlers=[{"sink": ORMLogHandler(url), "filter": check_orm_log, "enqueue": enqueue}])
    
    