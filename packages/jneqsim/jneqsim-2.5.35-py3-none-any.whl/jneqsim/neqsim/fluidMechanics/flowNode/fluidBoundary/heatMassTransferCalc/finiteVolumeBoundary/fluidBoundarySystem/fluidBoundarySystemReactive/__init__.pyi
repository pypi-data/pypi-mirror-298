
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.neqsim.fluidMechanics.flowNode.fluidBoundary.heatMassTransferCalc
import jneqsim.neqsim.fluidMechanics.flowNode.fluidBoundary.heatMassTransferCalc.finiteVolumeBoundary.fluidBoundarySystem
import typing



class FluidBoundarySystemReactive(jneqsim.neqsim.fluidMechanics.flowNode.fluidBoundary.heatMassTransferCalc.finiteVolumeBoundary.fluidBoundarySystem.FluidBoundarySystem):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, fluidBoundaryInterface: jneqsim.neqsim.fluidMechanics.flowNode.fluidBoundary.heatMassTransferCalc.FluidBoundaryInterface): ...
    def createSystem(self) -> None: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.fluidMechanics.flowNode.fluidBoundary.heatMassTransferCalc.finiteVolumeBoundary.fluidBoundarySystem.fluidBoundarySystemReactive")``.

    FluidBoundarySystemReactive: typing.Type[FluidBoundarySystemReactive]
