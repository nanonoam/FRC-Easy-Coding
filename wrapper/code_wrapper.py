from typing import Tuple
from validators.code_validator import Commands, isMoveCommand

directions = {
    Commands.TURN_LEFT: "Direction.LEFT",
    Commands.TURN_RIGHT: "Direction.RIGHT",
}

java_commands = {
    Commands.FORWARD: "new MoveX(chassis, %s)",
    Commands.BACKWARD: "new MoveX(chassis, -%s)",
    Commands.TURN_LEFT: "new Turn(chassis, %s * -0.0174532925)",
    Commands.TURN_RIGHT: "new Turn(chassis, %s * 0.0174532925)",
}

def wrap_commands_to_java(commands: list[Tuple[Commands, int]]):
    
    java_commands_list = tuple((java_commands[command] % value) 
                          for command, value in commands)
    match len(java_commands_list):
        case 0:
            return
        case 1:
            java_code = "\t\t\treturn " + java_commands_list[0] + ";"
        case 2:
            java_code = "\t\t\treturn %s\n\t\t\t.andThen(%s);" % java_commands_list
        case _:
            java_code = (
    """
        return %s
        .andThen(%s)
        .andThen(""" % java_commands_list[:2]
    ) + ")\n\t\t\t.andThen(".join(java_commands_list[2:]) + ");"
    return java_code
        