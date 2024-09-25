
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.processSimulation.mechanicalDesign
import jneqsim.neqsim.processSimulation.mechanicalDesign.separator.sectionType
import jneqsim.neqsim.processSimulation.processEquipment
import typing



class SeparatorMechanicalDesign(jneqsim.neqsim.processSimulation.mechanicalDesign.MechanicalDesign):
    def __init__(self, processEquipmentInterface: jneqsim.neqsim.processSimulation.processEquipment.ProcessEquipmentInterface): ...
    def calcDesign(self) -> None: ...
    def displayResults(self) -> None: ...
    def readDesignSpecifications(self) -> None: ...
    def setDesign(self) -> None: ...

class GasScrubberMechanicalDesign(SeparatorMechanicalDesign):
    def __init__(self, processEquipmentInterface: jneqsim.neqsim.processSimulation.processEquipment.ProcessEquipmentInterface): ...
    def calcDesign(self) -> None: ...
    def readDesignSpecifications(self) -> None: ...
    def setDesign(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.processSimulation.mechanicalDesign.separator")``.

    GasScrubberMechanicalDesign: typing.Type[GasScrubberMechanicalDesign]
    SeparatorMechanicalDesign: typing.Type[SeparatorMechanicalDesign]
    sectionType: jneqsim.neqsim.processSimulation.mechanicalDesign.separator.sectionType.__module_protocol__
